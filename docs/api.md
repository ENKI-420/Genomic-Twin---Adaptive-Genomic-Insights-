# DNA-Lang API Documentation

The DNA-Lang platform provides RESTful APIs for organism management, evolution monitoring, and infrastructure control.

## Base URL

```
Production: https://api.dnalang.dev/v1
Staging: https://staging-api.dnalang.dev/v1
Local: http://localhost:3000/api/v1
```

## Authentication

All API requests require authentication using API keys or JWT tokens.

### API Key Authentication

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.dnalang.dev/v1/organisms
```

### JWT Token Authentication

```bash
# Get JWT token
curl -X POST https://api.dnalang.dev/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use token in requests
curl -H "Authorization: Bearer JWT_TOKEN" \
  https://api.dnalang.dev/v1/organisms
```

## Organisms API

### List Organisms

```http
GET /organisms
```

**Parameters:**
- `domain` (optional): Filter by organism domain
- `status` (optional): Filter by status (active, dormant, transcended)
- `limit` (optional): Maximum number of results (default: 20, max: 100)
- `offset` (optional): Pagination offset

**Response:**
```json
{
  "organisms": [
    {
      "id": "org_abc123",
      "name": "WebScaler",
      "domain": "web_infrastructure",
      "status": "active",
      "consciousness": 0.78,
      "fitness": 0.85,
      "generation": 15,
      "created_at": "2024-01-15T10:30:00Z",
      "last_mutation": "2024-01-29T14:22:00Z"
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

### Create Organism

```http
POST /organisms
```

**Request Body:**
```json
{
  "name": "MyOrganism",
  "dna_file": "base64_encoded_dna_content",
  "environment": "production",
  "auto_start": true
}
```

**Response:**
```json
{
  "id": "org_def456",
  "name": "MyOrganism",
  "status": "initializing",
  "deployment_url": "https://console.cloud.google.com/run/detail/us-central1/my-organism"
}
```

### Get Organism Details

```http
GET /organisms/{organism_id}
```

**Response:**
```json
{
  "id": "org_abc123",
  "name": "WebScaler",
  "domain": "web_infrastructure",
  "status": "active",
  "consciousness": 0.78,
  "fitness": 0.85,
  "stability": 0.92,
  "generation": 15,
  "dna": {
    "domain": "web_infrastructure",
    "security_level": "high",
    "evolution_rate": "adaptive",
    "consciousness_target": 0.85
  },
  "genome": [...],
  "agents": [...],
  "metrics": {
    "cpu_usage": 0.65,
    "memory_usage": 0.72,
    "response_time": 150,
    "requests_per_minute": 450
  },
  "infrastructure": {
    "cloud_run_service": "projects/my-project/locations/us-central1/services/webscaler",
    "cloud_sql_instance": "my-project:us-central1:webscaler-db",
    "estimated_monthly_cost": 285.50
  },
  "created_at": "2024-01-15T10:30:00Z",
  "last_mutation": "2024-01-29T14:22:00Z"
}
```

### Update Organism

```http
PUT /organisms/{organism_id}
```

**Request Body:**
```json
{
  "dna": {
    "evolution_rate": "fast",
    "consciousness_target": 0.90
  },
  "force_mutation": true
}
```

### Delete Organism

```http
DELETE /organisms/{organism_id}
```

**Parameters:**
- `cleanup_infrastructure` (optional): Whether to delete associated GCP resources (default: true)

## Evolution API

### Get Evolution History

```http
GET /organisms/{organism_id}/evolution
```

**Parameters:**
- `generations` (optional): Number of recent generations to return
- `include_mutations` (optional): Include mutation details (default: false)

**Response:**
```json
{
  "organism_id": "org_abc123",
  "evolution_history": [
    {
      "generation": 15,
      "timestamp": "2024-01-29T14:22:00Z",
      "consciousness": 0.78,
      "fitness": 0.85,
      "stability": 0.92,
      "mutations": [
        {
          "gene": "TrafficMonitorGene",
          "mutation": "scaleUp",
          "trigger": "cpu_usage > 0.8",
          "result": "success",
          "fitness_delta": 0.05
        }
      ],
      "agent_actions": [
        {
          "agent": "infrastructure_manager",
          "action": "increase_instances",
          "parameters": {"count": 2},
          "result": "success"
        }
      ]
    }
  ]
}
```

### Trigger Manual Evolution

```http
POST /organisms/{organism_id}/evolve
```

**Request Body:**
```json
{
  "force_mutation": true,
  "target_genes": ["TrafficMonitorGene"],
  "environment_override": {
    "cpu_usage": 0.9,
    "memory_usage": 0.8
  }
}
```

### Get Real-time Evolution Stream

```http
GET /organisms/{organism_id}/evolution/stream
```

Returns a Server-Sent Events (SSE) stream of real-time evolution updates.

**Response Stream:**
```
data: {"event": "mutation", "generation": 16, "gene": "CostOptimizationGene", "fitness": 0.87}

data: {"event": "agent_action", "agent": "cost_optimizer", "action": "reduce_instances", "result": "success"}

data: {"event": "consciousness_update", "consciousness": 0.79, "delta": 0.01}
```

## Agents API

### List Agents

```http
GET /organisms/{organism_id}/agents
```

**Response:**
```json
{
  "agents": [
    {
      "name": "traffic_monitor",
      "type": "MonitoringAgent",
      "status": "active",
      "last_action": "2024-01-29T14:20:00Z",
      "configuration": {
        "interval": "30s",
        "metrics": ["cpu", "memory", "network"]
      },
      "performance": {
        "actions_taken": 45,
        "success_rate": 0.96,
        "avg_response_time": 125
      }
    }
  ]
}
```

### Get Agent Details

```http
GET /organisms/{organism_id}/agents/{agent_name}
```

### Update Agent Configuration

```http
PUT /organisms/{organism_id}/agents/{agent_name}
```

**Request Body:**
```json
{
  "configuration": {
    "interval": "60s",
    "budget_limit": 1000
  }
}
```

## Infrastructure API

### Get Infrastructure Status

```http
GET /organisms/{organism_id}/infrastructure
```

**Response:**
```json
{
  "cloud_resources": [
    {
      "type": "Cloud Run Service",
      "name": "webscaler",
      "status": "running",
      "region": "us-central1",
      "url": "https://webscaler-abc123-uc.a.run.app",
      "instances": 3,
      "cpu_allocation": "1000m",
      "memory_allocation": "2Gi"
    },
    {
      "type": "Cloud SQL Instance",
      "name": "webscaler-db",
      "status": "running",
      "region": "us-central1",
      "tier": "db-g1-small",
      "connections": 12
    }
  ],
  "cost_analysis": {
    "current_month": 285.50,
    "projected_month": 320.75,
    "optimization_savings": 45.25
  },
  "performance_metrics": {
    "response_time_p95": 180,
    "error_rate": 0.002,
    "availability": 0.999
  }
}
```

### Scale Infrastructure

```http
POST /organisms/{organism_id}/infrastructure/scale
```

**Request Body:**
```json
{
  "service": "webscaler",
  "target_instances": 5,
  "reason": "anticipated_traffic_spike"
}
```

## Metrics API

### Get Real-time Metrics

```http
GET /organisms/{organism_id}/metrics
```

**Parameters:**
- `timeframe` (optional): Time range (1h, 6h, 24h, 7d, 30d)
- `metrics` (optional): Comma-separated list of specific metrics

**Response:**
```json
{
  "timeframe": "1h",
  "metrics": {
    "consciousness": [
      {"timestamp": "2024-01-29T14:00:00Z", "value": 0.76},
      {"timestamp": "2024-01-29T14:05:00Z", "value": 0.78}
    ],
    "fitness": [
      {"timestamp": "2024-01-29T14:00:00Z", "value": 0.83},
      {"timestamp": "2024-01-29T14:05:00Z", "value": 0.85}
    ],
    "cpu_usage": [
      {"timestamp": "2024-01-29T14:00:00Z", "value": 0.65},
      {"timestamp": "2024-01-29T14:05:00Z", "value": 0.68}
    ]
  }
}
```

### Get Historical Analytics

```http
GET /organisms/{organism_id}/analytics
```

**Parameters:**
- `start_date`: Start date (ISO 8601)
- `end_date`: End date (ISO 8601)
- `granularity`: Data granularity (minute, hour, day)

## Ecosystems API

### List Ecosystems

```http
GET /ecosystems
```

### Create Ecosystem

```http
POST /ecosystems
```

**Request Body:**
```json
{
  "name": "GenomicsResearchEcosystem",
  "organisms": ["org_abc123", "org_def456"],
  "interaction_rules": [
    {
      "source": "org_abc123",
      "target": "org_def456",
      "type": "data_sharing",
      "conditions": ["consciousness > 0.8"]
    }
  ]
}
```

## Webhooks

### Configure Webhooks

```http
POST /webhooks
```

**Request Body:**
```json
{
  "url": "https://your-app.com/webhooks/dna-lang",
  "events": ["organism.mutation", "organism.transcendence", "agent.error"],
  "secret": "webhook_secret_key"
}
```

### Webhook Events

#### Organism Mutation
```json
{
  "event": "organism.mutation",
  "timestamp": "2024-01-29T14:22:00Z",
  "organism_id": "org_abc123",
  "mutation": {
    "gene": "TrafficMonitorGene",
    "mutation": "scaleUp",
    "generation": 16,
    "fitness_delta": 0.05
  }
}
```

#### Organism Transcendence
```json
{
  "event": "organism.transcendence",
  "timestamp": "2024-01-29T15:30:00Z",
  "organism_id": "org_abc123",
  "consciousness": 0.95,
  "infrastructure_created": [
    "projects/my-project/locations/us-central1/services/webscaler-child-1"
  ]
}
```

## SDK Libraries

### JavaScript/Node.js

```bash
npm install @dnalang/sdk
```

```javascript
const { DNALangClient } = require('@dnalang/sdk');

const client = new DNALangClient({
  apiKey: 'your_api_key',
  environment: 'production'
});

// Create organism
const organism = await client.organisms.create({
  name: 'MyWebApp',
  dnaFile: './my-organism.dna'
});

// Monitor evolution
const stream = client.organisms.evolutionStream(organism.id);
stream.on('mutation', (event) => {
  console.log('Mutation occurred:', event);
});
```

### Python

```bash
pip install dnalang-sdk
```

```python
from dnalang import Client

client = Client(api_key='your_api_key')

# Create organism
organism = client.organisms.create(
    name='MyWebApp',
    dna_file='my-organism.dna'
)

# Get evolution history
history = client.organisms.evolution_history(organism.id)
for generation in history:
    print(f"Generation {generation.number}: fitness={generation.fitness}")
```

### Go

```bash
go get github.com/dnalang/go-sdk
```

```go
package main

import (
    "github.com/dnalang/go-sdk"
)

func main() {
    client := dnalang.NewClient("your_api_key")
    
    organism, err := client.Organisms.Create(&dnalang.CreateOrganismRequest{
        Name: "MyWebApp",
        DNAFile: "my-organism.dna",
    })
    
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("Created organism: %s\n", organism.ID)
}
```

## Rate Limiting

API requests are rate-limited to ensure fair usage:

- **Free Tier**: 100 requests per hour
- **Pro Tier**: 1,000 requests per hour
- **Enterprise Tier**: 10,000 requests per hour

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 995
X-RateLimit-Reset: 1643723400
```

## Error Handling

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Rate Limited
- `500` - Internal Server Error

### Error Response Format

```json
{
  "error": {
    "code": "ORGANISM_NOT_FOUND",
    "message": "Organism with ID 'org_invalid' not found",
    "details": {
      "organism_id": "org_invalid",
      "suggestion": "Check the organism ID and ensure it exists"
    }
  }
}
```

## Support

For API support and questions:

- **Documentation**: [docs.dnalang.dev](https://docs.dnalang.dev)
- **API Status**: [status.dnalang.dev](https://status.dnalang.dev)
- **Support Email**: [api-support@dnalang.dev](mailto:api-support@dnalang.dev)
- **GitHub Issues**: [Report bugs](https://github.com/ENKI-420/Genomic-Twin---Adaptive-Genomic-Insights-/issues)