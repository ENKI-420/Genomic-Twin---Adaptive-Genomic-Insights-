import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random
import requests
import json
import logging
import ssl
import hashlib
import os
import time
from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Tuple, Set, Union
from functools import lru_cache
import warnings
import re

# Make retrying optional
try:
    from retrying import retry
    RETRYING_AVAILABLE = True
except ImportError:
    RETRYING_AVAILABLE = False
    # Create a fallback for retry decorator
    def retry(*args, **kwargs):
        def decorator(func):
            def wrapper(*func_args, **func_kwargs):
                return func(*func_args, **func_kwargs)
            return wrapper
        # Handle both @retry and @retry(...) formats
        if len(args) == 1 and callable(args[0]):
            return decorator(args[0])
        return decorator

# Make fuzzywuzzy optional
try:
    from fuzzywuzzy import fuzz
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    FUZZYWUZZY_AVAILABLE = False
    # Create a fallback for fuzz
    class FuzzFallback:
        @staticmethod
        def token_set_ratio(a, b):
            # Simple string equality check as fallback
            return 100 if a.lower() == b.lower() else 0
    fuzz = FuzzFallback()

# Make geopy optional
try:
    from geopy.distance import geodesic
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False
    # Create a fallback for geodesic
    def geodesic(point1, point2):
        class Distance:
            def __init__(self):
                self.kilometers = 0
        return Distance()

# Make spacy optional
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    # Create a fallback for spacy
    class SpacyFallback:
        class Document:
            def __init__(self, text):
                self.text = text
                self.ents = []
                self.sents = [self]
        
        def load(self, model_name):
            return self
            
        def __call__(self, text):
            return self.Document(text)
    
    spacy = SpacyFallback()

# Make sklearn optional
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    # Create fallbacks for sklearn classes
    class RandomForestClassifierFallback:
        def __init__(self, **kwargs):
            pass
            
        def predict_proba(self, X):
            import numpy as np
            # Always return 0.5 probability (neutral)
            return np.array([[0.5, 0.5]] * len(X))
    
    class TfidfVectorizerFallback:
        def __init__(self, **kwargs):
            pass
            
        def transform(self, texts):
            import numpy as np
            # Return an empty sparse matrix placeholder
            class SparseMatrix:
                def __init__(self, shape=(1, 1)):
                    self.shape = shape
            return SparseMatrix()
            
    RandomForestClassifier = RandomForestClassifierFallback
    TfidfVectorizer = TfidfVectorizerFallback

# Make joblib optional
try:
    import joblib
    JOBLIB_AVAILABLE = True
except ImportError:
    JOBLIB_AVAILABLE = False
    # Create a fallback for joblib functionality
    class JobLibFallback:
        @staticmethod
        def load(file_path):
            logger.warning(f"Joblib not available. Cannot load model from {file_path}")
            return None
            
        @staticmethod
        def dump(obj, file_path, compress=3):
            logger.warning(f"Joblib not available. Cannot save model to {file_path}")
            return None
    
    joblib = JobLibFallback()

# Make streamlit optional
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    # Create a fallback for streamlit's warning function
    class StreamlitFallback:
        def warning(self, message):
            logging.warning(f"Streamlit warning: {message}")
        
    st = StreamlitFallback()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure SSL context for secure API connections
ssl_context = ssl.create_default_context()
ssl_context.set_ciphers('HIGH:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!3DES:!MD5:!PSK')

# Try to load NLP model if available, otherwise provide graceful fallback
if SPACY_AVAILABLE:
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        logger.warning("Spacy language model not found. NLP features will be limited.")
        nlp = None
else:
    logger.warning("Spacy not installed. NLP features will be unavailable.")
    nlp = None

# Data classes for structured trial information
@dataclass
class Location:
    facility: str
    city: str
    state: str
    country: str
    zip_code: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    
    def get_coordinates(self) -> Tuple[Optional[float], Optional[float]]:
        """Return location coordinates as a tuple."""
        return (self.lat, self.lon)
    
    def __str__(self) -> str:
        return f"{self.facility}, {self.city}, {self.state} {self.zip_code}, {self.country}"

@dataclass
class Eligibility:
    gender: str
    min_age: int
    max_age: int
    criteria_text: str
    inclusion_criteria: List[str]
    exclusion_criteria: List[str]
    biomarkers: List[str]
    min_ecog: Optional[int] = None
    max_ecog: Optional[int] = None
    
    def __str__(self) -> str:
        age_criteria = f"Age: {self.min_age}-{self.max_age}" if self.max_age < 999 else f"Age: {self.min_age}+"
        return f"{self.gender}, {age_criteria}"

@dataclass
class ClinicalTrial:
    id: str
    title: str
    phase: str  
    status: str
    conditions: List[str]
    summary: str
    detailed_description: Optional[str]
    biomarkers: List[str]
    locations: List[Location]
    eligibility: Eligibility
    start_date: datetime
    primary_completion_date: Optional[datetime]
    study_type: str
    sponsor: str
    interventions: List[str]
    score: float = 0.0
    
    def __str__(self) -> str:
        return f"{self.title} (ID: {self.id}, Phase: {self.phase})"
class ClinicalTrialMatcher:
    """
    A comprehensive clinical trial matching system that finds and scores clinical trials
    based on patient profiles using real-world clinical trial registries, NLP for eligibility
    criteria extraction, and machine learning for trial scoring.
    """
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None, config_path: Optional[str] = None):
        """
        Initialize the clinical trial matcher with API keys and configuration settings.
        
        Parameters:
        -----------
        api_keys : dict, optional
            Dictionary containing API keys for various trial registries
            Example: {'ctgov': 'your_api_key', 'who': 'your_who_key', 'eu': 'your_eu_key'}
        config_path : str, optional
            Path to a JSON configuration file with API keys and settings
        """
        # Default API endpoints for clinical trial registries
        self.endpoints = {
            'clinicaltrials_gov': 'https://clinicaltrials.gov/api/v2/studies',
            'who_ictrp': 'https://apps.who.int/ictrp/search/',
            'eu_ctr': 'https://www.clinicaltrialsregister.eu/ctr-search/rest',
            'fhir': 'https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/'
        }
        
        # FHIR resource types
        self.fhir_resources = {
            'patient': 'Patient',
            'condition': 'Condition',
            'observation': 'Observation',
            'medication': 'MedicationRequest',
            'procedure': 'Procedure',
            'diagnostic_report': 'DiagnosticReport'
        }
        
        # Load API keys from config file if provided, else use passed keys or empty dict
        self.api_keys = {} 
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.api_keys = config.get('api_keys', {})
            except (json.JSONDecodeError, OSError) as e:
                logger.error(f"Failed to load configuration from {config_path}: {e}")
        
        # Override with directly provided API keys if any
        if api_keys:
            self.api_keys.update(api_keys)
            
        # Initialize cache
        self._initialize_cache()
        
        # Load ML scoring model or create a new one
        self._initialize_scoring_model()
    def _initialize_cache(self):
        """Initialize in-memory cache for trial data."""
        self.cache = {}
        self.cache_expiry = {}
        self.CACHE_DURATION = 24 * 60 * 60  # Cache duration in seconds (24 hours)
        
    def _generate_cache_key(self, patient_profile: Dict[str, Any]) -> str:
        """
        Generate a unique cache key for a patient profile.
        
        Parameters:
        -----------
        patient_profile : dict
            Patient profile to generate cache key for
            
        Returns:
        --------
        str
            SHA-256 hash of the patient profile
        """
        # Convert the patient profile to a stable string representation
        profile_str = json.dumps(patient_profile, sort_keys=True)
        
        # Generate a hash of the string
        cache_key = hashlib.sha256(profile_str.encode()).hexdigest()
        
        return cache_key
    
    def _check_cache(self, cache_key: str) -> Optional[List[ClinicalTrial]]:
        """
        Check if a valid cache entry exists for the given key.
        
        Parameters:
        -----------
        cache_key : str
            Cache key to check
            
        Returns:
        --------
        Optional[List[ClinicalTrial]]
            List of cached trials if found and valid, None otherwise
        """
        # Check if key exists in cache
        if cache_key not in self.cache:
            return None
            
        # Check if cache entry has expired
        if time.time() > self.cache_expiry.get(cache_key, 0):
            # Remove expired entry
            if cache_key in self.cache:
                del self.cache[cache_key]
            if cache_key in self.cache_expiry:
                del self.cache_expiry[cache_key]
            return None
            
        # Return cached trials
        return self.cache[cache_key]
        
    def _update_cache(self, cache_key: str, trials: List[ClinicalTrial]) -> None:
        """
        Update the cache with a new entry.
        
        Parameters:
        -----------
        cache_key : str
            Cache key to update
        trials : List[ClinicalTrial]
            Trial data to cache
        """
        # Store trials in cache
        self.cache[cache_key] = trials
        
        # Set expiry time
        self.cache_expiry[cache_key] = time.time() + self.CACHE_DURATION
        
        # Clean old cache entries if cache is too large (optional)
        if len(self.cache) > 100:  # Limit cache to 100 entries
            # Find oldest entries
            oldest_keys = sorted(self.cache_expiry, key=self.cache_expiry.get)[:10]
            # Remove oldest entries
            for key in oldest_keys:
                if key in self.cache:
                    del self.cache[key]
                if key in self.cache_expiry:
                    del self.cache_expiry[key]
        self.CACHE_DURATION = 24 * 60 * 60  # Cache duration in seconds (24 hours)
    
    def _initialize_scoring_model(self):
        """Initialize or load the machine learning scoring model."""
        model_path = os.path.join(os.path.dirname(__file__), 'data', 'trial_matching_model.joblib')
        if os.path.exists(model_path):
            try:
                if JOBLIB_AVAILABLE:
                    self.model = joblib.load(model_path)
                    self.tfidf_vectorizer = joblib.load(os.path.join(os.path.dirname(__file__), 'data', 'tfidf_vectorizer.joblib'))
                    logger.info("Loaded machine learning scoring model")
                else:
                    logger.warning("Joblib not available. Cannot load ML model. Creating new model.")
                    self._create_new_model()
            except (OSError, ValueError) as e:
                logger.warning(f"Error loading ML model: {e}. Creating new model.")
                self._create_new_model()
        else:
            self._create_new_model()
    
    def _create_new_model(self):
        """Create a new ML model for trial scoring if none exists."""
        if SKLEARN_AVAILABLE:
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.tfidf_vectorizer = TfidfVectorizer(max_features=5000)
            logger.info("Created new machine learning scoring model")
        else:
            self.model = RandomForestClassifier()
            self.tfidf_vectorizer = TfidfVectorizer()
            logger.warning("Sklearn not available. Using dummy ML model instead.")
        
    def find_matching_trials(self, patient_profile: Dict[str, Any]) -> List[ClinicalTrial]:
        """
        Find clinical trials matching a patient's profile using real-world APIs.
        
        Parameters:
        -----------
        patient_profile : dict
            Dictionary containing patient information such as:
            - diagnosis (list of diagnosis codes or conditions)
            - biomarkers (list of biomarker statuses)
            - age (patient age in years)
            - gender (patient gender)
            - location (tuple of latitude, longitude)
            - ecog_status (ECOG performance status)
            - prior_treatments (list of previous treatments)
            
        Returns:
        --------
        list of ClinicalTrial
            Sorted list of clinical trials matching the patient profile
        """
        # Check cache first
        cache_key = self._generate_cache_key(patient_profile)
        cached_trials = self._check_cache(cache_key)
        if cached_trials:
            logger.info(f"Retrieved {len(cached_trials)} trials from cache")
            return cached_trials
        
        # Validate patient profile
        self._validate_patient_profile(patient_profile)
        
        # Fetch trials from multiple registries
        all_trials = []
        
        try:
            # Query ClinicalTrials.gov
            ctgov_trials = self._query_clinicaltrials_gov(patient_profile)
            all_trials.extend(ctgov_trials)
            logger.info(f"Retrieved {len(ctgov_trials)} trials from ClinicalTrials.gov")
            
            # Add queries to other registries when available
            # who_trials = self._query_who_ictrp(patient_profile)
            # all_trials.extend(who_trials)
            # eu_trials = self._query_eu_ctr(patient_profile)
            # all_trials.extend(eu_trials)
        except Exception as e:
            logger.error(f"Error querying clinical trial registries: {e}")
            # If APIs fail, fall back to simulated data but log a warning
            logger.warning("Falling back to simulated trial data")
            return self._generate_simulated_trials(patient_profile)
        
        # Score and sort trials based on patient matching
        scored_trials = []
        for trial in all_trials:
            trial_score = self._score_trial(trial, patient_profile)
            scored_trials.append(trial)
        
        # Sort by score (descending)
        sorted_trials = sorted(scored_trials, key=lambda x: x.score, reverse=True)
        
        # Cache the results
        self._update_cache(cache_key, sorted_trials)
        
        return sorted_trials
    
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def _query_clinicaltrials_gov(self, patient_profile: Dict[str, Any]) -> List[ClinicalTrial]:
        """
        Query the ClinicalTrials.gov API for trials matching the patient profile.
        
        Parameters:
        -----------
        patient_profile : dict
            Patient profile information
            
        Returns:
        --------
        list of ClinicalTrial
            List of clinical trials from ClinicalTrials.gov
        """
        # Construct search parameters
        params = {
            'format': 'json',
            'pageSize': 100  # Adjust as needed
        }
        
        # Add conditions/diagnosis
        if 'diagnosis' in patient_profile and patient_profile['diagnosis']:
            condition_term = ' OR '.join(patient_profile['diagnosis'])
            params['query.cond'] = condition_term
        
        # Add phase filter if specified
        if 'phase' in patient_profile and patient_profile['phase']:
            params['filter.phase'] = patient_profile['phase']
        
        # Add status filter (default to recruiting/not yet recruiting)
        params['filter.overall_status'] = 'RECRUITING,NOT_YET_RECRUITING,ACTIVE_NOT_RECRUITING'
        
        # Add API key if available
        headers = {}
        if 'ctgov' in self.api_keys:
            headers['Authorization'] = f"Bearer {self.api_keys['ctgov']}"
        
        # Make API request
        try:
            response = requests.get(
                self.endpoints['clinicaltrials_gov'],
                params=params,
                headers=headers,
                timeout=10,
                verify=ssl_context
            )
            
            if response.status_code != 200:
                logger.error(f"ClinicalTrials.gov API error: {response.status_code} - {response.text}")
                return []
            
            # Parse the response
            data = response.json()
            return self._parse_ctgov_response(data)
            
        except requests.RequestException as e:
            logger.error(f"Error querying ClinicalTrials.gov: {e}")
            return []
    
    def _parse_ctgov_response(self, response_data: Dict[str, Any]) -> List[ClinicalTrial]:
        """
        Parse the response from ClinicalTrials.gov API into ClinicalTrial objects.
        
        Parameters:
        -----------
        response_data : dict
            JSON response from the ClinicalTrials.gov API
            
        Returns:
        --------
        list of ClinicalTrial
            List of parsed clinical trials
        """
        trials = []
        
        # Check if the response contains studies
        studies = response_data.get('studies', [])
        if not studies:
            logger.warning("No studies found in ClinicalTrials.gov response")
            return trials
            
        # Process each study from the API response
        for study in studies:
            try:
                # Extract protocol section data
                protocol = study.get('protocolSection', {})
                id_module = protocol.get('identificationModule', {})
                status_module = protocol.get('statusModule', {})
                design_module = protocol.get('designModule', {})
                condition_module = protocol.get('conditionsModule', {})
                desc_module = protocol.get('descriptionModule', {})
                eligibility_module = protocol.get('eligibilityModule', {})
                contact_locations_module = protocol.get('contactsLocationsModule', {})
                intervention_module = protocol.get('interventionModule', {})
                sponsor_module = protocol.get('sponsorCollaboratorsModule', {})
                
                # Extract biomarkers if available
                biomarker_module = protocol.get('biospecDescriptionModule', {})
                biomarkers = []
                biomarker_descriptions = biomarker_module.get('biospecDescription', '')
                
                # Extract biomarkers using NLP if description exists
                if biomarker_descriptions and nlp:
                    biomarkers = self._extract_biomarkers(biomarker_descriptions)
                
                # Process locations
                locations = []
                for location_data in contact_locations_module.get('locations', []):
                    try:
                        facility = location_data.get('facility', '')
                        city = location_data.get('city', '')
                        state = location_data.get('state', '')
                        country = location_data.get('country', '')
                        zip_code = location_data.get('zip', '')
                        
                        # Try to get coordinates if available
                        lat, lon = None, None
                        geo_point = location_data.get('geoPoint', {})
                        if geo_point:
                            lat = geo_point.get('lat')
                            lon = geo_point.get('lon')
                        
                        locations.append(Location(
                            facility=facility,
                            city=city,
                            state=state,
                            country=country,
                            zip_code=zip_code,
                            lat=lat,
                            lon=lon
                        ))
                    except Exception as e:
                        logger.warning(f"Error processing location: {e}")
                
                # Process eligibility criteria
                gender = eligibility_module.get('sex', 'All')
                min_age_str = eligibility_module.get('minimumAge', '0 Years')
                max_age_str = eligibility_module.get('maximumAge', '100 Years')
                
                # Parse age values
                min_age = self._parse_age_string(min_age_str)
                max_age = self._parse_age_string(max_age_str)
                
                # Extract inclusion/exclusion criteria text
                criteria_text = eligibility_module.get('eligibilityCriteria', '')
                
                # Use NLP to extract structured eligibility criteria
                inclusion_criteria, exclusion_criteria, extracted_biomarkers, ecog_data = self._extract_eligibility_criteria(criteria_text)
                
                # Add extracted biomarkers to the biomarkers list
                if extracted_biomarkers:
                    biomarkers.extend(extracted_biomarkers)
                
                # Create Eligibility object
                eligibility = Eligibility(
                    gender=gender,
                    min_age=min_age,
                    max_age=max_age,
                    criteria_text=criteria_text,
                    inclusion_criteria=inclusion_criteria,
                    exclusion_criteria=exclusion_criteria,
                    biomarkers=biomarkers,
                    min_ecog=ecog_data.get('min_ecog'),
                    max_ecog=ecog_data.get('max_ecog')
                )
                
                # Parse dates
                start_date_str = status_module.get('startDateStruct', {}).get('date', '')
                completion_date_str = status_module.get('primaryCompletionDateStruct', {}).get('date', '')
                
                # Convert date strings to datetime objects
                start_date = self._parse_date_string(start_date_str)
                completion_date = self._parse_date_string(completion_date_str) if completion_date_str else None
                
                # Extract conditions/diseases
                conditions = condition_module.get('conditions', [])
                
                # Extract interventions
                interventions = []
                for intervention in intervention_module.get('interventions', []):
                    intervention_name = intervention.get('name', '')
                    if intervention_name:
                        interventions.append(intervention_name)
                
                # Extract sponsor information
                sponsor_name = sponsor_module.get('leadSponsor', {}).get('name', 'Unknown')
                
                # Create ClinicalTrial object
                trial = ClinicalTrial(
                    id=id_module.get('nctId', ''),
                    title=id_module.get('briefTitle', ''),
                    phase=design_module.get('phases', ['N/A'])[0] if design_module.get('phases') else 'N/A',
                    status=status_module.get('overallStatus', 'Unknown'),
                    conditions=conditions,
                    summary=desc_module.get('briefSummary', ''),
                    detailed_description=desc_module.get('detailedDescription', ''),
                    biomarkers=biomarkers,
                    locations=locations,
                    eligibility=eligibility,
                    start_date=start_date,
                    primary_completion_date=completion_date,
                    study_type=design_module.get('studyType', 'Unknown'),
                    sponsor=sponsor_name,
                    interventions=interventions,
                    score=0.0  # Initial score, will be updated later
                )
                
                trials.append(trial)
                
            except Exception as e:
                logger.error(f"Error parsing study data: {e}")
                continue
        
        return trials

    def _parse_age_string(self, age_string: str) -> int:
        """Parse age string (e.g., '18 Years') to integer age in years."""
        try:
            if not age_string:
                return 0
                
            # Extract numeric part
            numeric_part = ''.join(c for c in age_string if c.isdigit() or c == '.')
            if not numeric_part:
                return 0
                
            # Convert to float first to handle decimal ages
            age_value = float(numeric_part)
            
            # Convert to years if needed
            if 'month' in age_string.lower():
                age_value = age_value / 12
            elif 'week' in age_string.lower():
                age_value = age_value / 52
            elif 'day' in age_string.lower():
                age_value = age_value / 365
                
            return int(age_value)
        except Exception:
            logger.warning(f"Could not parse age string: {age_string}")
            return 0
            
    def _parse_date_string(self, date_string: str) -> Optional[datetime]:
        """Parse date string from ClinicalTrials.gov API."""
        try:
            if not date_string:
                return None
                
            # Format is usually 'YYYY-MM-DD'
            return datetime.strptime(date_string, '%Y-%m-%d')
        except ValueError:
            try:
                # Try alternative format with just year and month
                return datetime.strptime(date_string, '%Y-%m')
            except ValueError:
                try:
                    # Try just year format
                    return datetime.strptime(date_string, '%Y')
                except ValueError:
                    logger.warning(f"Could not parse date string: {date_string}")
                    return None
                    
    def _extract_biomarkers(self, text: str) -> List[str]:
        """Extract biomarkers from text using NLP."""
        if not nlp or not text:
            return []
            
        biomarkers = []
        # Common biomarker patterns
        biomarker_patterns = [
            r"(?i)(EGFR|ALK|ROS1|BRAF|KRAS|NRAS|HER2|PIK3CA|BRCA|PD-L1|TMB|MSI|dMMR|IDH1|IDH2)[\s-]*(exon|V600|G12C|positive|negative|mutation|amplification|fusion|\d+%|\+|-)?",
            r"(?i)(ER|PR|AR|TP53|MET|RET|FGFR|CDK|MDM2)[\s-]*(positive|negative|mutation|amplification|fusion|\d+%|\+|-)?",
            r"(?i)(CD|PD-1|CTLA-4|LAG-3|TIM-3)\d+[\s-]*(positive|negative|\+|-)?",
            r"(?i)(high|low|positive|negative|amplified)[\s-]*(TMB|MSI|PD-L1|HER2)",
            r"(?i)(deletion|amplification|mutation|fusion|translocation)\s+(?:of|in)\s+([A-Z0-9-]+)"
        ]
        
        # Apply each pattern
        for pattern in biomarker_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                biomarker = match.group(0).strip()
                if biomarker and len(biomarker) > 2:  # Avoid single character matches
                    biomarkers.append(biomarker)
        
        # Use spaCy for additional biomarker extraction
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["GENE", "PROTEIN", "CHEMICAL", "DISEASE"]:
                # Check if it might be a biomarker
                if any(term in ent.text.lower() for term in ["mutation", "positive", "negative", "expression", "amplification"]):
                    biomarkers.append(ent.text)
        
        # Remove duplicates and return
        return list(set(biomarkers))
        
    def _extract_eligibility_criteria(self, criteria_text: str) -> Tuple[List[str], List[str], List[str], Dict[str, Optional[int]]]:
        """
        Extract structured eligibility criteria using NLP.
        
        Returns:
        --------
        Tuple containing:
        - List of inclusion criteria
        - List of exclusion criteria
        - List of biomarkers
        - Dict with ECOG performance status info
        """
        inclusion = []
        exclusion = []
        biomarkers = []
        ecog_info = {'min_ecog': None, 'max_ecog': None}
        
        if not criteria_text:
            return inclusion, exclusion, biomarkers, ecog_info
            
        # Split text into inclusion and exclusion sections
        sections = re.split(r"(?i)inclusion criteria:|exclusion criteria:", criteria_text)
        
        if len(sections) > 1:
            # Process inclusion criteria
            inclusion_text = sections[1].strip()
            if len(sections) > 2:
                # Find the end of the inclusion section
                inclusion_text = inclusion_text.split("Exclusion Criteria:", 1)[0]
                
            # Extract individual criteria
            inclusion = self._extract_criteria_items(inclusion_text)
            
            # Extract biomarkers from inclusion criteria
            inclusion_biomarkers = self._extract_biomarkers(inclusion_text)
            if inclusion_biomarkers:
                biomarkers.extend(inclusion_biomarkers)
                
        if len(sections) > 2:
            # Process exclusion criteria
            exclusion_text = sections[2].strip()
            exclusion = self._extract_criteria_items(exclusion_text)
            
            # Extract biomarkers from exclusion criteria (some trials specify biomarkers in exclusion)
            exclusion_biomarkers = self._extract_biomarkers(exclusion_text)
            if exclusion_biomarkers:
                biomarkers.extend(exclusion_biomarkers)
                
        # Extract ECOG performance status
        ecog_info = self._extract_ecog_status(criteria_text)
        
        return inclusion, exclusion, list(set(biomarkers)), ecog_info
        
    def _extract_criteria_items(self, text: str) -> List[str]:
        """Extract individual criteria items from text."""
        # First try to split by bullet points or numbered items
        items = re.split(r'\n\s*[\-\*•]|\n\s*\d+\.|\n\s*-\s+', text)
        
        # If that didn't work well, try splitting by newlines
        if len(items) <= 1:
            items = [item.strip() for item in text.split('\n') if item.strip()]
            
        # If we still have just one item, try splitting by sentences
        # If we still have just one item, try splitting by sentences
        if len(items) <= 1 and nlp and SPACY_AVAILABLE:
            doc = nlp(text)
            items = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        elif len(items) <= 1 and not SPACY_AVAILABLE:
            # Simple fallback when spaCy is not available - split by periods
            items = [item.strip() for item in text.replace('\n', ' ').split('.') if item.strip()]
        # Remove empty items and clean up
        items = [item.strip() for item in items if item.strip()]
        
        return items
        
    def _extract_ecog_status(self, text: str) -> Dict[str, Optional[int]]:
        """Extract ECOG performance status from eligibility criteria text."""
        result = {'min_ecog': None, 'max_ecog': None}
        
        if not text:
            return result
            
        # Common patterns for ECOG performance status
        ecog_patterns = [
            r"(?i)ECOG\s*(performance\s*status|\s*PS|\s*status)?\s*(\d+)[-–]?(\d+)?",
            r"(?i)(ECOG|Eastern Cooperative Oncology Group)\s*(performance\s*status|\s*PS|\s*status)?\s*(\d+)[-–]?(\d+)?",
            r"(?i)(performance\s*status|PS)\s*(\d+)[-–]?(\d+)?"
        ]
        
        for pattern in ecog_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                # Extract numbers from the match
                groups = match.groups()
                ecog_numbers = [int(g) for g in groups if g and g.isdigit()]
                
                if ecog_numbers:
                    if len(ecog_numbers) == 1:
                        # If only one number is found, it's likely the maximum allowed ECOG
                        result['max_ecog'] = ecog_numbers[0]
                        # Assume min is 0 if only one value provided
                        result['min_ecog'] = 0
                    elif len(ecog_numbers) >= 2:
                        # If range is provided, set both min and max
                        result['min_ecog'] = min(ecog_numbers)
                        result['max_ecog'] = max(ecog_numbers)
        
        # If found in text but not through regex, use NLP methods
        if not result['max_ecog'] and nlp:
            doc = nlp(text)
            for sent in doc.sents:
                sent_text = sent.text.lower()
                if 'ecog' in sent_text or 'performance status' in sent_text:
                    # Look for digits in the sentence
                    digits = re.findall(r'\d+', sent_text)
                    if digits:
                        ecog_values = [int(d) for d in digits if int(d) <= 5]  # ECOG is typically 0-5
                        if ecog_values:
                            result['max_ecog'] = max(ecog_values)
                            if len(ecog_values) > 1:
                                result['min_ecog'] = min(ecog_values)
                            else:
                                result['min_ecog'] = 0
        
        return result
            
    def _score_trial(self, trial: ClinicalTrial, patient_profile: Dict[str, Any]) -> ClinicalTrial:
        """
        Score a clinical trial based on its match with the patient profile.
        
        Parameters:
        -----------
        trial : ClinicalTrial
            The clinical trial to be scored
        patient_profile : dict
            The patient profile to match against
            
        Returns:
        --------
        ClinicalTrial
            The same trial with updated score
        """
        # Initialize score components
        condition_score = 0.0
        biomarker_score = 0.0
        location_score = 0.0
        demographics_score = 0.0
        phase_score = 0.0
        
        # 1. Condition/diagnosis matching (30% of total score)
        if 'diagnosis' in patient_profile and patient_profile['diagnosis'] and trial.conditions:
            # Use fuzzy matching to find best match between patient diagnosis and trial conditions
            if FUZZYWUZZY_AVAILABLE:
                max_condition_match = max(
                    fuzz.token_set_ratio(d, c) 
                    for d in patient_profile['diagnosis'] 
                    for c in trial.conditions
                ) / 100.0
            else:
                # Basic matching fallback when fuzzywuzzy is not available
                matches = []
                for d in patient_profile['diagnosis']:
                    for c in trial.conditions:
                        if d.lower() in c.lower() or c.lower() in d.lower():
                            matches.append(0.8)  # 80% match for substring
                        elif d.lower() == c.lower():
                            matches.append(1.0)  # 100% match for exact match
                        else:
                            matches.append(0.0)  # No match
                max_condition_match = max(matches) if matches else 0.0
            condition_score = max_condition_match * 0.3
        
        # 2. Biomarker matching (25% of total score)
        if 'biomarkers' in patient_profile and patient_profile['biomarkers'] and trial.biomarkers:
            # Calculate percentage of patient biomarkers that match trial biomarkers
            patient_biomarkers = set(patient_profile['biomarkers'])
            trial_biomarkers = set(trial.biomarkers)
            
            # Check for direct matches
            direct_matches = patient_biomarkers.intersection(trial_biomarkers)
            
            # Check for fuzzy matches for biomarkers that didn't directly match
            fuzzy_matches = 0
            remaining_patient = patient_biomarkers - direct_matches
            remaining_trial = trial_biomarkers - direct_matches
            
            if remaining_patient and remaining_trial:
                for p_bio in remaining_patient:
                    for t_bio in remaining_trial:
                        if FUZZYWUZZY_AVAILABLE and fuzz.token_set_ratio(p_bio, t_bio) > 80:  # 80% similarity threshold
                            fuzzy_matches += 1
                            break
                        # Basic fallback when fuzzywuzzy is not available
                        elif not FUZZYWUZZY_AVAILABLE and (p_bio.lower() in t_bio.lower() or t_bio.lower() in p_bio.lower()):
                            fuzzy_matches += 1
                            break
            
            # Calculate final biomarker score
            if patient_biomarkers:
                biomarker_match_rate = (len(direct_matches) + fuzzy_matches) / len(patient_biomarkers)
                biomarker_score = biomarker_match_rate * 0.25
        
        # 3. Geographic location matching (15% of total score)
        if 'location' in patient_profile and patient_profile['location'] and trial.locations:
            # Find minimum distance between patient and any trial location
            min_distance_km = float('inf')
            patient_lat, patient_lon = patient_profile['location']
            for location in trial.locations:
                if location.lat is not None and location.lon is not None:
                    if GEOPY_AVAILABLE:
                        distance = geodesic(
                            (patient_lat, patient_lon), 
                            (location.lat, location.lon)
                        ).kilometers
                    else:
                        # Simple distance fallback when geopy is not available
                        # Just check if they're in the same country/state
                        distance = 0 if location.country == patient_profile.get('country', '') else 500
                    min_distance_km = min(min_distance_km, distance)
                    min_distance_km = min(min_distance_km, distance)
            
            # Calculate location score (inverse of distance, max at 500km)
            if min_distance_km < float('inf'):
                # Closer locations score higher, with diminishing returns after 100km
                location_score = 0.15 * max(0, 1 - (min_distance_km / 500))
            else:
                location_score = 0
        
        # 4. Demographics matching (age, gender, ECOG) (20% of total score)
        demographics_score = 0.0
        
        # Age matching
        if 'age' in patient_profile:
            patient_age = patient_profile['age']
            if trial.eligibility.min_age <= patient_age <= trial.eligibility.max_age:
                demographics_score += 0.1
            elif patient_age < trial.eligibility.min_age or patient_age > trial.eligibility.max_age:
                # Age is exclusionary, return zero score immediately
                trial.score = 0.0
                return trial
        
        # Gender matching
        if 'gender' in patient_profile:
            patient_gender = patient_profile['gender'].lower()
            trial_gender = trial.eligibility.gender.lower()
            
            if trial_gender == 'all' or patient_gender == trial_gender or (
                patient_gender in ['male', 'm'] and trial_gender in ['male', 'm']) or (
                patient_gender in ['female', 'f'] and trial_gender in ['female', 'f']):
                demographics_score += 0.05
            else:
                # Gender is exclusionary, return zero score immediately
                trial.score = 0.0
                return trial
        
        # ECOG performance status
        if 'ecog_status' in patient_profile and trial.eligibility.max_ecog is not None:
            patient_ecog = patient_profile['ecog_status']
            min_ecog = trial.eligibility.min_ecog if trial.eligibility.min_ecog is not None else 0
            max_ecog = trial.eligibility.max_ecog
            
            if min_ecog <= patient_ecog <= max_ecog:
                demographics_score += 0.05
            else:
                # ECOG is exclusionary, return zero score immediately
                trial.score = 0.0
                return trial
        
        # 5. Trial phase preference (10% of total score)
        if 'phase_preference' in patient_profile:
            pref = patient_profile['phase_preference']
            if pref == 'late' and trial.phase in ['Phase 3', 'Phase 4', '3', '4']:
                phase_score = 0.1
            elif pref == 'early' and trial.phase in ['Phase 1', 'Phase 2', '1', '2']:
                phase_score = 0.1
            elif str(pref) == str(trial.phase).replace('Phase ', ''):
                phase_score = 0.1
        else:
            # Default preference for later phase trials if not specified
            if trial.phase in ['Phase 3', 'Phase 4', '3', '4']:
                phase_score = 0.08
            elif trial.phase in ['Phase 2', '2']:
                phase_score = 0.06
            elif trial.phase in ['Phase 1', '1']:
                phase_score = 0.04
        
        # Calculate total score
        total_score = condition_score + biomarker_score + location_score + demographics_score + phase_score
        
        # Apply machine learning model if available and all required features are present
        # Apply machine learning model if available and all required features are present
        if hasattr(self, 'model') and hasattr(self, 'tfidf_vectorizer'):
            try:
                if SKLEARN_AVAILABLE:
                    ml_score = self._calculate_ml_score(trial, patient_profile)
                    
                    # Weighted average of rule-based and ML-based scores
                    total_score = 0.7 * total_score + 0.3 * ml_score
                else:
                    # If sklearn isn't available, just use the rule-based score
                    logger.debug("Sklearn not available. Using rule-based score only.")
            except Exception as e:
                logger.warning(f"Error calculating ML score: {e}. Using rule-based score only.")
        # Update the trial's score and return
        trial.score = round(total_score, 2)
        return trial
    
    def _calculate_ml_score(self, trial: ClinicalTrial, patient_profile: Dict[str, Any]) -> float:
        """Calculate a match score using the machine learning model."""
        # Extract features for ML model
        features = {}
        
        # Text features
        trial_text = f"{trial.title} {trial.summary} {' '.join(trial.conditions)} {' '.join(trial.biomarkers)}"
        
        # Patient text
        patient_text = f"{' '.join(patient_profile.get('diagnosis', []))} {' '.join(patient_profile.get('biomarkers', []))}"
        
        # Vectorize text
        if patient_text and trial_text:
            # Use TF-IDF vectorizer
            combined_text = patient_text + " " + trial_text
            text_vector = self.tfidf_vectorizer.transform([combined_text])
            
            # Add numeric features
            features = {
                'age_match': 1 if ('age' in patient_profile and 
                                  trial.eligibility.min_age <= patient_profile['age'] <= trial.eligibility.max_age) else 0,
                'gender_match': 1 if ('gender' in patient_profile and 
                                      (trial.eligibility.gender.lower() == 'all' or 
                                       patient_profile['gender'].lower() == trial.eligibility.gender.lower())) else 0,
                'phase': float(str(trial.phase).replace('Phase ', '').split()[0]) if str(trial.phase).replace('Phase ', '').split()[0].isdigit() else 0
            }
            
            # Use the model to predict a score (between 0 and 1)
            try:
                # Convert features to the format expected by the model
                feature_array = pd.DataFrame([features])
                
                # Get prediction from model
                prediction = self.model.predict_proba(feature_array)[:, 1][0]
                return float(prediction)
            except Exception as e:
                logger.error(f"Error in ML prediction: {e}")
                return 0.5  # Default to middle score on error
        
        return 0.5  # Default score
        
    def _validate_patient_profile(self, patient_profile: Dict[str, Any]) -> None:
        """
        Validate the patient profile data structure and contents.
        Raises ValueError if the profile is invalid.
        
        Parameters:
        -----------
        patient_profile : dict
            Patient profile to validate
        """
        if not isinstance(patient_profile, dict):
            raise ValueError("Patient profile must be a dictionary")
        
        # Check for minimum required fields
        required_fields = []  # No strictly required fields, but we validate types of provided fields
        
        # Validate diagnosis field if provided
        if 'diagnosis' in patient_profile:
            if not isinstance(patient_profile['diagnosis'], list):
                raise ValueError("Diagnosis must be a list of conditions")
        
        # Validate biomarkers if provided
        if 'biomarkers' in patient_profile:
            if not isinstance(patient_profile['biomarkers'], list):
                raise ValueError("Biomarkers must be a list of biomarker values")
        
        # Validate age if provided
        if 'age' in patient_profile:
            if not isinstance(patient_profile['age'], (int, float)) or patient_profile['age'] < 0:
                raise ValueError("Age must be a positive number")
        
        # Validate gender if provided
        if 'gender' in patient_profile:
            if not isinstance(patient_profile['gender'], str):
                raise ValueError("Gender must be a string")
        
        # Validate location if provided
        if 'location' in patient_profile:
            if not isinstance(patient_profile['location'], tuple) or len(patient_profile['location']) != 2:
                raise ValueError("Location must be a tuple of (latitude, longitude)")
            lat, lon = patient_profile['location']
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                raise ValueError("Invalid latitude/longitude values")
        
        # Validate ECOG status if provided
        if 'ecog_status' in patient_profile:
            if not isinstance(patient_profile['ecog_status'], int) or not (0 <= patient_profile['ecog_status'] <= 5):
                raise ValueError("ECOG status must be an integer from 0 to 5")
        
        # Validate prior treatments if provided
        if 'prior_treatments' in patient_profile:
            if not isinstance(patient_profile['prior_treatments'], list):
                raise ValueError("Prior treatments must be a list of treatment names")
        
        # Validate phase preference if provided
        if 'phase_preference' in patient_profile:
            valid_phases = ['early', 'late', 1, 2, 3, 4, '1', '2', '3', '4']
            if patient_profile['phase_preference'] not in valid_phases:
                raise ValueError(f"Phase preference must be one of {valid_phases}")
        
        logger.info("Patient profile validation successful")

    # FHIR integration methods for Epic EHR
    def get_patient_data_from_epic(self, patient_id: str, access_token: str) -> Dict[str, Any]:
        """
        Retrieve patient data from Epic EHR using FHIR APIs.
        
        Parameters:
        -----------
        patient_id : str
            The patient's FHIR resource ID
        access_token : str
            OAuth2 access token for authenticating with the Epic FHIR API
            
        Returns:
        --------
        dict
            Comprehensive patient data for trial matching
        """
        patient_profile = {
            'diagnosis': [],
            'biomarkers': [],
            'medications': [],
            'age': None,
            'gender': None,
            'ecog_status': None,
            'prior_treatments': []
        }
        
        try:
            # Set up headers with authentication
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json'
            }
            
            # Get basic patient demographics
            patient_data = self._get_fhir_resource(
                resource_type=self.fhir_resources['patient'],
                resource_id=patient_id,
                headers=headers
            )
            
            if patient_data:
                # Extract gender
                patient_profile['gender'] = patient_data.get('gender', '')
                
                # Calculate age from birthDate
                birth_date = patient_data.get('birthDate')
                if birth_date:
                    birth_datetime = datetime.strptime(birth_date, '%Y-%m-%d')
                    age = (datetime.now() - birth_datetime).days // 365
                    patient_profile['age'] = age
            
            # Get conditions/diagnoses
            conditions = self._get_fhir_resources(
                resource_type=self.fhir_resources['condition'],
                query_params={'patient': patient_id, 'status': 'active,confirmed'},
                headers=headers
            )
            
            for condition in conditions:
                # Extract condition codes (ICD-10, SNOMED CT, etc.)
                if 'code' in condition and 'coding' in condition['code']:
                    for coding in condition['code']['coding']:
                        code = coding.get('code')
                        system = coding.get('system')
                        display = coding.get('display')
                        
                        if code:
                            # Add condition to list
                            if display:
                                patient_profile['diagnosis'].append(display)
                            else:
                                patient_profile['diagnosis'].append(code)
            
            # Get lab results and biomarkers
            observations = self._get_fhir_resources(
                resource_type=self.fhir_resources['observation'],
                query_params={'patient': patient_id, 'category': 'laboratory'},
                headers=headers
            )
            
            for observation in observations:
                # Check if this observation is related to a biomarker
                if 'code' in observation and 'coding' in observation['code']:
                    for coding in observation['code']['coding']:
                        code = coding.get('code')
                        display = coding.get('display')
                        
                        # Identify biomarker tests
                        biomarker_terms = ['her2', 'er', 'pr', 'egfr', 'alk', 'ros1', 'braf', 'pd-l1', 'msi', 
                                          'tmb', 'brca', 'kras', 'nras', 'met', 'ret', 'ntrk']
                        
                        if display and any(term in display.lower() for term in biomarker_terms):
                            # Extract result value
                            if 'valueCodeableConcept' in observation:
                                value = observation['valueCodeableConcept'].get('text', '')
                                if value:
                                    biomarker = f"{display}: {value}"
                                    patient_profile['biomarkers'].append(biomarker)
                            elif 'valueQuantity' in observation:
                                value = observation['valueQuantity'].get('value', '')
                                unit = observation['valueQuantity'].get('unit', '')
                                if value is not None:
                                    biomarker = f"{display}: {value}{unit}"
                                    patient_profile['biomarkers'].append(biomarker)
            
            # Get medication history
            medications = self._get_fhir_resources(
                resource_type=self.fhir_resources['medication'],
                query_params={'patient': patient_id},
                headers=headers
            )
            
            for medication in medications:
                if 'medicationCodeableConcept' in medication and 'coding' in medication['medicationCodeableConcept']:
                    for coding in medication['medicationCodeableConcept']['coding']:
                        display = coding.get('display')
                        if display:
                            patient_profile['prior_treatments'].append(display)
            
            # Try to get ECOG status from latest observation
            ecog_observations = self._get_fhir_resources(
                resource_type=self.fhir_resources['observation'],
                query_params={'patient': patient_id, 'code': 'http://loinc.org|89247-1'},  # LOINC code for ECOG
                headers=headers
            )
            
            if ecog_observations:
                # Sort by date to get the most recent
                latest_ecog = sorted(
                    ecog_observations, 
                    key=lambda x: x.get('effectiveDateTime', ''), 
                    reverse=True
                )[0]
                
                if 'valueInteger' in latest_ecog:
                    patient_profile['ecog_status'] = latest_ecog['valueInteger']
                elif 'valueQuantity' in latest_ecog:
                    patient_profile['ecog_status'] = int(latest_ecog['valueQuantity'].get('value', 0))
            
            # Remove duplicates from lists
            patient_profile['diagnosis'] = list(set(patient_profile['diagnosis']))
            patient_profile['biomarkers'] = list(set(patient_profile['biomarkers']))
            patient_profile['prior_treatments'] = list(set(patient_profile['prior_treatments']))
            
            logger.info(f"Successfully retrieved patient data from Epic EHR for patient {patient_id}")
            return patient_profile
            
        except Exception as e:
            logger.error(f"Error retrieving patient data from Epic EHR: {e}")
            return patient_profile
    
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def _get_fhir_resource(self, resource_type: str, resource_id: str, headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Get a single FHIR resource by ID.
        
        Parameters:
        -----------
        resource_type : str
            The FHIR resource type (e.g., 'Patient', 'Condition')
        resource_id : str
            The FHIR resource ID
        headers : dict
            Headers for the HTTP request
            
        Returns:
        --------
        dict
            FHIR resource as JSON
        """
        url = f"{self.endpoints['fhir']}{resource_type}/{resource_id}"
        
        try:
            response = requests.get(
                url,
                headers=headers,
                timeout=10,
                verify=ssl_context
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Failed to retrieve FHIR resource {resource_type}/{resource_id}: {response.status_code}")
                return {}
                
        except requests.RequestException as e:
            logger.error(f"Error requesting FHIR resource {resource_type}/{resource_id}: {e}")
            return {}
    
    @retry(stop_max_attempt_number=3, wait_fixed=2000)
    def _get_fhir_resources(self, resource_type: str, query_params: Dict[str, str], headers: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Search for FHIR resources using query parameters.
        
        Parameters:
        -----------
        resource_type : str
            The FHIR resource type (e.g., 'Patient', 'Condition')
        query_params : dict
            Query parameters for the search
        headers : dict
            Headers for the HTTP request
            
        Returns:
        --------
        list
            List of FHIR resources as JSON
        """
        url = f"{self.endpoints['fhir']}{resource_type}"
        
        try:
            response = requests.get(
                url,
                params=query_params,
                headers=headers,
                timeout=10,
                verify=ssl_context
            )
            
            if response.status_code == 200:
                data = response.json()
                # Extract entries from bundle
                if 'entry' in data:
                    return [entry['resource'] for entry in data['entry']]
                return []
            else:
                logger.warning(f"Failed to retrieve FHIR resources {resource_type}: {response.status_code}")
                return []
                
        except requests.RequestException as e:
            logger.error(f"Error requesting FHIR resources {resource_type}: {e}")
        except requests.RequestException as e:
            logger.error(f"Error requesting FHIR resources {resource_type}: {e}")
            return []

def generate_mock_trials(cancer_type=None, phase=None, location=None, intervention_type=None, min_participants=0):
    """
    Generate mock clinical trial data with optional filtering parameters.
    
    Parameters:
    -----------
    cancer_type : str, optional
        Filter trials by cancer type
    phase : int or str, optional
        Filter trials by phase (1, 2, 3, 4, 'early', or 'late')
    location : str, optional
        Filter trials by location
    intervention_type : str, optional
        Filter trials by intervention type
    min_participants : int, optional
        Minimum number of participants (default: 0)
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing mock clinical trial data
    """
    # Define possible values for each field
    cancer_types = ['Lung Cancer', 'Breast Cancer', 'Leukemia', 'Prostate Cancer', 
                   'Colorectal Cancer', 'Melanoma', 'Lymphoma', 'Pancreatic Cancer',
                   'Ovarian Cancer', 'Glioblastoma']
    phases = [1, 2, 3, 4]
    locations = ['United States', 'Europe', 'Asia', 'Global', 'Canada', 'Australia']
    statuses = ['Recruiting', 'Active', 'Completed', 'Suspended', 'Not yet recruiting']
    intervention_types = ['Drug', 'Biological', 'Device', 'Procedure', 'Radiation', 'Combination']
    sponsors = ['National Cancer Institute', 'Memorial Sloan Kettering', 'MD Anderson',
               'Mayo Clinic', 'Dana-Farber', 'Genentech', 'Novartis', 'Pfizer',
               'Merck', 'AstraZeneca', 'Roche', 'BMS', 'GSK']
    
    # Filter based on input parameters
    if cancer_type:
        cancer_types = [c for c in cancer_types if cancer_type.lower() in c.lower()]
    
    if phase:
        if isinstance(phase, str):
            if phase.lower() == 'early':
                phases = [1, 2]
            elif phase.lower() == 'late':
                phases = [3, 4]
        else:
            phases = [phase]
    
    if location:
        locations = [loc for loc in locations if location.lower() in loc.lower()]
    
    if intervention_type:
        intervention_types = [i for i in intervention_types if intervention_type.lower() in i.lower()]
    
    # Generate 20-50 random trials
    num_trials = random.randint(20, 50)
    
    # Create empty lists for each column
    trial_ids = []
    titles = []
    trial_cancer_types = []
    trial_phases = []
    trial_locations = []
    trial_statuses = []
    trial_interventions = []
    trial_sponsors = []
    start_dates = []
    end_dates = []
    participant_counts = []
    
    # Generate random data for each trial
    for i in range(num_trials):
        # Generate a unique trial ID
        trial_id = f"NCT{random.randint(1000000, 9999999)}"
        
        # Select a random cancer type
        selected_cancer = random.choice(cancer_types)
        
        # Select a random phase
        selected_phase = random.choice(phases)
        
        # Generate a title based on the cancer type and intervention
        selected_intervention = random.choice(intervention_types)
        if selected_intervention == 'Drug' or selected_intervention == 'Biological':
            drug_name = f"{random.choice(['A', 'B', 'C', 'D', 'E', 'M', 'N', 'P', 'R', 'Z'])}{random.choice(['av', 'en', 'ol', 'ib', 'ab', 'ix', 'mab', 'zol', 'tin'])}-{random.randint(100, 999)}"
            title = f"Study of {drug_name} in Patients With {selected_cancer}"
            intervention_detail = f"{selected_intervention}: {drug_name}"
        else:
            title = f"{selected_intervention} Therapy for {selected_cancer} - Phase {selected_phase} Trial"
            intervention_detail = selected_intervention
        
        # Generate random dates
        current_date = datetime.now()
        start_date = current_date - timedelta(days=random.randint(0, 1095))  # Up to 3 years ago
        duration = random.randint(180, 1095)  # 6 months to 3 years
        end_date = start_date + timedelta(days=duration)
        
        # Generate a random number of participants
        participants = random.randint(10, 1000)
        
        # Skip trials with fewer than min_participants
        if participants < min_participants:
            continue
        
        # Append values to lists
        trial_ids.append(trial_id)
        titles.append(title)
        trial_cancer_types.append(selected_cancer)
        trial_phases.append(selected_phase)
        trial_locations.append(random.choice(locations))
        trial_statuses.append(random.choice(statuses))
        trial_interventions.append(intervention_detail)
        trial_sponsors.append(random.choice(sponsors))
        start_dates.append(start_date)
        end_dates.append(end_date)
        participant_counts.append(participants)
    
    # Create a DataFrame
    df = pd.DataFrame({
        'Trial ID': trial_ids,
        'Title': titles,
        'Cancer Type': trial_cancer_types,
        'Phase': trial_phases,
        'Location': trial_locations,
        'Status': trial_statuses,
        'Intervention': trial_interventions,
        'Sponsor': trial_sponsors,
        'Start Date': start_dates,
        'End Date': end_dates,
        'Participants': participant_counts
    })
    
    return df


def generate_summary_statistics(trials_df):
    """Generate summary statistics for clinical trials."""
    # Count trials by phase
    phase_counts = trials_df['Phase'].value_counts().reset_index()
    phase_counts.columns = ['Phase', 'Number of Trials']
    
    # Count trials by cancer type
    cancer_counts = trials_df['Cancer Type'].value_counts().reset_index()
    cancer_counts.columns = ['Cancer Type', 'Number of Trials']
    
    # Average participants by phase
    avg_participants = trials_df.groupby('Phase')['Participants'].mean().reset_index()
    avg_participants.columns = ['Phase', 'Average Participants']
    
    # Count trials by status
    status_counts = trials_df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Number of Trials']
    
    # Return as a dictionary of dataframes
    return {
        'phase_counts': phase_counts,
        'cancer_counts': cancer_counts,
        'avg_participants': avg_participants,
        'status_counts': status_counts
    }

def generate_efficacy_data(trials_df):
    """Generate simulated efficacy data for the clinical trials."""
    # Select completed trials for efficacy data
    completed_trials = trials_df[trials_df['Status'] == 'Completed']
    
    if completed_trials.empty:
        # If no completed trials, use a sample of all trials
        completed_trials = trials_df.sample(min(5, len(trials_df)))
    
    # Create empty lists for efficacy metrics
    trial_ids = []
    response_rates = []
    survival_months = []
    p_values = []
    hazard_ratios = []
    
    # Generate random efficacy data for each trial
    for _, trial in completed_trials.iterrows():
        trial_ids.append(trial['Trial ID'])
        
        # Higher phase trials tend to have better efficacy
        phase_factor = trial['Phase'] / 4.0
        
        # Generate simulated response rate (higher for higher phases)
        response_rate = random.uniform(0.1, 0.3) + (phase_factor * 0.4)
        response_rates.append(round(response_rate, 2))
        
        # Generate simulated survival in months (higher for higher phases)
        base_survival = random.uniform(6, 12)
        survival = base_survival + (phase_factor * 24)
        survival_months.append(round(survival, 1))
        
        # Generate p-value (lower for higher phases, indicating stronger evidence)
        p_value = random.uniform(0.001, 0.2) * (1 - (phase_factor * 0.5))
        p_values.append(round(p_value, 3))
        
        # Generate hazard ratio (lower is better, indicating reduced risk)
        hr_base = random.uniform(0.5, 1.0)
        hazard_ratio = hr_base - (phase_factor * 0.3)
        hazard_ratios.append(round(hazard_ratio, 2))
    
    # Create a DataFrame
    efficacy_df = pd.DataFrame({
        'Trial ID': trial_ids,
        'Response Rate': response_rates,
        'Median Survival (months)': survival_months,
        'P-value': p_values,
        'Hazard Ratio': hazard_ratios
    })
    
    # Join with trial information
    efficacy_df = efficacy_df.merge(
        completed_trials[['Trial ID', 'Cancer Type', 'Phase', 'Intervention']], 
        on='Trial ID'
    )
    
    return efficacy_df

# Add an alias for generate_mock_trials function
generate_trial_data = generate_mock_trials

def generate_timeline_data(trials_df):
    """Generate timeline data for visualizing trial durations and milestones."""
    # Sample up to 15 trials for the timeline view
    timeline_trials = trials_df.sample(min(15, len(trials_df)))
    
    # Create lists for the timeline data
    trial_ids = []
    titles = []
    start_dates = []
    end_dates = []
    current_phases = []
    next_milestones = []
    milestone_dates = []
    
    # Generate timeline data for each trial
    for _, trial in timeline_trials.iterrows():
        trial_ids.append(trial['Trial ID'])
        titles.append(trial['Title'])
        start_dates.append(trial['Start Date'])
        end_dates.append(trial['End Date'])
        
        # Current phase
        current_phases.append(f"Phase {trial['Phase']}")
        
        # Generate a future milestone
        if trial['Status'] == 'Completed':
            next_milestone = "Final Results Publication"
            # Publication typically happens 6-12 months after completion
            milestone_date = trial['End Date'] + timedelta(days=random.randint(180, 365))
        elif trial['Status'] == 'Recruiting':
            next_milestone = "Enrollment Complete"
            # Calculate a date between now and the end date
            today = datetime.now()
            days_until_end = (trial['End Date'] - today).days
            if days_until_end > 0:
                milestone_date = today + timedelta(days=random.randint(30, days_until_end))
            else:
                milestone_date = today + timedelta(days=random.randint(30, 180))
        else:
            next_milestone = "Interim Analysis"
            # Calculate a date between start and end
            total_days = (trial['End Date'] - trial['Start Date']).days
            milestone_date = trial['Start Date'] + timedelta(days=int(total_days * 0.6))
        
        next_milestones.append(next_milestone)
        milestone_dates.append(milestone_date)
    
    # Create a DataFrame
    timeline_df = pd.DataFrame({
        'Trial ID': trial_ids,
        'Title': titles,
        'Start Date': start_dates,
        'End Date': end_dates,
        'Current Phase': current_phases,
        'Next Milestone': next_milestones,
        'Milestone Date': milestone_dates
    })
    
    return timeline_df
# For backward compatibility
def clinical():
    """Legacy function, use find_trials() instead."""
    if STREAMLIT_AVAILABLE:
        st.warning("The clinical() function is deprecated. Please use find_trials() instead.")
    else:
        logging.warning("The clinical() function is deprecated. Please use find_trials() instead.")
    return find_trials()

def find_trials(cancer_type=None, phase=None, location=None, intervention_type=None, min_participants=0, patient_profile=None, use_real_api=False, fhir_access_token=None):
    """
    Find clinical trials matching specified criteria using either simulated data or real trial registry APIs.
    
    This function provides backward compatibility with the original functionality while also supporting
    the advanced ClinicalTrialMatcher features when appropriate parameters are provided.
    
    Parameters:
    -----------
    cancer_type : str, optional
        Type of cancer to filter trials for
    phase : int or str, optional
        Clinical trial phase (1, 2, 3, 4, or 'early'/'late')
    location : str, optional
        Geographic location to filter trials for
    intervention_type : str, optional
        Type of intervention (Drug, Biological, Device, etc.)
    min_participants : int, optional
        Minimum number of participants for the trial
    patient_profile : dict, optional
        Comprehensive patient profile for advanced matching with ClinicalTrialMatcher
        Should include fields like 'diagnosis', 'biomarkers', 'age', 'gender', 'location', 'ecog_status'
    use_real_api : bool, optional
        Whether to use real clinical trial registry APIs (True) or simulated data (False)
    fhir_access_token : str, optional
        OAuth2 access token for FHIR API access to retrieve patient data from Epic EHR
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing clinical trial information
    """
    # If use_real_api is True and we have a patient profile, use the advanced ClinicalTrialMatcher
    if use_real_api and patient_profile:
        try:
            logger.info("Using ClinicalTrialMatcher with real API data")
            
            # Initialize the ClinicalTrialMatcher
            matcher = ClinicalTrialMatcher()
            
            # If a partial patient profile is provided, try to enhance it with FHIR data if available
            if fhir_access_token and 'patient_id' in patient_profile:
                try:
                    fhir_patient_data = matcher.get_patient_data_from_epic(
                        patient_id=patient_profile['patient_id'],
                        access_token=fhir_access_token
                    )
                    
                    # Merge FHIR patient data with provided patient profile
                    # Patient-provided data takes precedence over FHIR data
                    for key, value in fhir_patient_data.items():
                        if key not in patient_profile or not patient_profile[key]:
                            patient_profile[key] = value
                            
                    logger.info("Enhanced patient profile with FHIR data")
                except Exception as e:
                    logger.warning(f"Could not retrieve FHIR patient data: {e}")
            
            # Ensure patient profile has basic fields
            if 'diagnosis' not in patient_profile and cancer_type:
                patient_profile['diagnosis'] = [cancer_type]
                
            if 'phase_preference' not in patient_profile and phase:
                patient_profile['phase_preference'] = phase
                
            # Use ClinicalTrialMatcher to find matching trials
            matching_trials = matcher.find_matching_trials(patient_profile)
            
            # Convert ClinicalTrial objects to the DataFrame format expected by the original function
            return _convert_trials_to_dataframe(matching_trials)
            
        except Exception as e:
            logger.error(f"Error using ClinicalTrialMatcher: {e}")
            logger.warning("Falling back to simulated trial data")
            # Fall back to the original approach on error
    
    # Use the original approach with simulated data
    logger.info("Using simulated clinical trial data")
    return generate_trial_data(
        cancer_type=cancer_type,
        phase=phase,
        location=location,
        intervention_type=intervention_type,
        min_participants=min_participants
    )

def _convert_trials_to_dataframe(trials):
    """
    Convert a list of ClinicalTrial objects to a pandas DataFrame with the same
    structure as the original find_trials() function.
    
    Parameters:
    -----------
    trials : list of ClinicalTrial
        List of ClinicalTrial objects from ClinicalTrialMatcher
        
    Returns:
    --------
    pandas.DataFrame
        DataFrame with the same structure as generate_trial_data()
    """
    # Create empty lists for each column
    trial_ids = []
    titles = []
    cancer_types = []
    phases = []
    locations = []
    statuses = []
    interventions = []
    sponsors = []
    start_dates = []
    end_dates = []
    participant_counts = []
    
    # Extract data from each ClinicalTrial object
    for trial in trials:
        trial_ids.append(trial.id)
        titles.append(trial.title)
        
        # Join multiple conditions into a single string
        cancer_types.append(', '.join(trial.conditions))
        
        # Convert phase format
        phase_str = trial.phase
        if phase_str.startswith('Phase '):
            phase_str = phase_str.replace('Phase ', '')
        try:
            phases.append(int(phase_str) if phase_str.isdigit() else phase_str)
        except:
            phases.append(phase_str)
        
        # Get the first location or 'Unknown'
        location_str = 'Unknown'
        if trial.locations and len(trial.locations) > 0:
            first_loc = trial.locations[0]
            location_str = f"{first_loc.city}, {first_loc.state}" if (first_loc.city and first_loc.state) else \
                          first_loc.country if first_loc.country else 'Unknown'
        locations.append(location_str)
        
        statuses.append(trial.status)
        
        # Join multiple interventions into a single string
        interventions.append(', '.join(trial.interventions) if trial.interventions else 'Not specified')
        
        sponsors.append(trial.sponsor)
        
        # Start and end dates
        start_dates.append(trial.start_date if trial.start_date else None)
        end_dates.append(trial.primary_completion_date if trial.primary_completion_date else None)
        
        # Generate a reasonable participant count (not available in the ClinicalTrial object)
        # This is simulated since the real data doesn't always provide this
        if trial.phase in ['Phase 1', '1']:
            participant_counts.append(random.randint(10, 100))
        elif trial.phase in ['Phase 2', '2']:
            participant_counts.append(random.randint(50, 300))
        elif trial.phase in ['Phase 3', '3']:
            participant_counts.append(random.randint(200, 1000))
        elif trial.phase in ['Phase 4', '4']:
            participant_counts.append(random.randint(500, 5000))
        else:
            participant_counts.append(random.randint(20, 200))
    
    # Create a DataFrame
    df = pd.DataFrame({
        'Trial ID': trial_ids,
        'Title': titles,
        'Cancer Type': cancer_types,
        'Phase': phases,
        'Location': locations,
        'Status': statuses,
        'Intervention': interventions,
        'Sponsor': sponsors,
        'Start Date': start_dates,
        'End Date': end_dates,
        'Participants': participant_counts
    })
    
    return df
