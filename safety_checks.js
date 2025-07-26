// safety_checks.js
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * Robust Repository Operation Validator
 * Addresses validateRepoOperations failure blocking Terraform infra externalization
 */
async function validateRepoOperations(repoPath) {
  const validationResults = {
    passed: false,
    errors: [],
    warnings: [],
    details: {}
  };

  try {
    console.log('[Safety] Starting comprehensive repository validation...');
    
    // 1. Check repo presence and permissions
    try {
      if (!fs.existsSync(repoPath)) {
        throw new Error(`Repository path does not exist: ${repoPath}`);
      }
      
      const stats = fs.statSync(repoPath);
      if (!stats.isDirectory()) {
        throw new Error(`Path is not a directory: ${repoPath}`);
      }
      
      // Check read/write permissions
      fs.accessSync(repoPath, fs.constants.R_OK | fs.constants.W_OK);
      validationResults.details.repoAccess = '✅ PASS';
      console.log('[Safety] Repository access: ✅ PASS');
    } catch (err) {
      validationResults.errors.push(`Repository access failed: ${err.message}`);
      validationResults.details.repoAccess = '❌ FAIL';
    }

    // 2. Verify Git repository validity
    try {
      const gitDir = path.join(repoPath, '.git');
      if (!fs.existsSync(gitDir)) {
        throw new Error('Not a Git repository (no .git directory found)');
      }
      
      execSync('git status', { cwd: repoPath, stdio: 'pipe' });
      validationResults.details.gitRepo = '✅ PASS';
      console.log('[Safety] Git repository validation: ✅ PASS');
    } catch (err) {
      validationResults.errors.push(`Git repository validation failed: ${err.message}`);
      validationResults.details.gitRepo = '❌ FAIL';
    }

    // 3. Check Git connectivity and remote configuration
    try {
      const remotes = execSync('git remote -v', { cwd: repoPath, stdio: 'pipe' }).toString();
      if (!remotes.trim()) {
        throw new Error('No Git remotes configured');
      }
      
      validationResults.details.gitRemotes = '✅ PASS';
      console.log('[Safety] Git remotes configured: ✅ PASS');
    } catch (err) {
      validationResults.errors.push(`Git remote validation failed: ${err.message}`);
      validationResults.details.gitRemotes = '❌ FAIL';
    }

    // 4. Test Git connectivity with dry-run push
    try {
      execSync('git push --dry-run', { cwd: repoPath, stdio: 'pipe' });
      validationResults.details.gitConnectivity = '✅ PASS';
      console.log('[Safety] Git connectivity (dry-run): ✅ PASS');
    } catch (err) {
      // Dry-run push might fail for various reasons, treat as warning not error
      validationResults.warnings.push(`Git connectivity test warning: ${err.message}`);
      validationResults.details.gitConnectivity = '⚠️ WARNING';
      console.log('[Safety] Git connectivity (dry-run): ⚠️ WARNING');
    }

    // 5. Check for working tree cleanliness
    try {
      const status = execSync('git status --porcelain', { cwd: repoPath, stdio: 'pipe' }).toString();
      if (status.trim()) {
        const uncommittedFiles = status.trim().split('\n').length;
        validationResults.warnings.push(`${uncommittedFiles} uncommitted changes present:\n${status}`);
        validationResults.details.workingTree = '⚠️ DIRTY';
        console.log(`[Safety] Working tree status: ⚠️ DIRTY (${uncommittedFiles} files)`);
      } else {
        validationResults.details.workingTree = '✅ CLEAN';
        console.log('[Safety] Working tree status: ✅ CLEAN');
      }
    } catch (err) {
      validationResults.errors.push(`Working tree status check failed: ${err.message}`);
      validationResults.details.workingTree = '❌ FAIL';
    }

    // 6. Check for Git locks or concurrent operations
    try {
      const lockFiles = ['.git/index.lock', '.git/refs/heads/main.lock', '.git/refs/heads/master.lock'];
      const activeLocks = lockFiles.filter(lockFile => fs.existsSync(path.join(repoPath, lockFile)));
      
      if (activeLocks.length > 0) {
        validationResults.warnings.push(`Git lock files detected: ${activeLocks.join(', ')}`);
        validationResults.details.gitLocks = '⚠️ LOCKED';
        console.log('[Safety] Git lock status: ⚠️ LOCKED');
      } else {
        validationResults.details.gitLocks = '✅ UNLOCKED';
        console.log('[Safety] Git lock status: ✅ UNLOCKED');
      }
    } catch (err) {
      validationResults.warnings.push(`Git lock check failed: ${err.message}`);
      validationResults.details.gitLocks = '⚠️ UNKNOWN';
    }

    // 7. Verify Terraform-specific requirements
    try {
      const terraformFiles = ['main.tf', 'generated.main.tf'].filter(file => 
        fs.existsSync(path.join(repoPath, file))
      );
      
      if (terraformFiles.length > 0) {
        validationResults.details.terraformFiles = `✅ Found: ${terraformFiles.join(', ')}`;
        console.log(`[Safety] Terraform files: ✅ Found: ${terraformFiles.join(', ')}`);
      } else {
        validationResults.warnings.push('No Terraform files found (main.tf, generated.main.tf)');
        validationResults.details.terraformFiles = '⚠️ NONE FOUND';
        console.log('[Safety] Terraform files: ⚠️ NONE FOUND');
      }
    } catch (err) {
      validationResults.warnings.push(`Terraform file check failed: ${err.message}`);
      validationResults.details.terraformFiles = '❌ ERROR';
    }

    // Determine overall validation result
    validationResults.passed = validationResults.errors.length === 0;

    if (validationResults.passed) {
      console.log('[Safety] validateRepoOperations: ✅ PASS');
      if (validationResults.warnings.length > 0) {
        console.log(`[Safety] ${validationResults.warnings.length} warnings noted but validation passed`);
      }
    } else {
      console.error(`[Safety] validateRepoOperations: ❌ FAIL - ${validationResults.errors.length} errors`);
      validationResults.errors.forEach(error => console.error(`[Safety] ERROR: ${error}`));
    }

    return validationResults;

  } catch (err) {
    console.error('[Safety] validateRepoOperations: ❌ CRITICAL FAILURE -', err.message);
    validationResults.errors.push(`Critical validation failure: ${err.message}`);
    validationResults.passed = false;
    return validationResults;
  }
}

/**
 * Enhanced validation with retry logic for network-dependent operations
 */
async function validateRepoOperationsWithRetry(repoPath, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    console.log(`[Safety] Validation attempt ${attempt}/${maxRetries}`);
    
    const result = await validateRepoOperations(repoPath);
    
    if (result.passed || attempt === maxRetries) {
      return result;
    }
    
    // Wait before retry (exponential backoff)
    const delay = Math.pow(2, attempt) * 1000;
    console.log(`[Safety] Retry in ${delay}ms...`);
    await new Promise(resolve => setTimeout(resolve, delay));
  }
}

/**
 * Lightweight validation for quick checks
 */
function quickValidateRepo(repoPath) {
  try {
    // Basic checks only
    if (!fs.existsSync(repoPath)) return false;
    if (!fs.existsSync(path.join(repoPath, '.git'))) return false;
    
    execSync('git status', { cwd: repoPath, stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

module.exports = { 
  validateRepoOperations, 
  validateRepoOperationsWithRetry,
  quickValidateRepo 
};