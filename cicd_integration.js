// cicd_integration.js
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { validateRepoOperations } = require('./safety_checks');

/**
 * CI/CD Integration Functions
 * Provides automated git operations and CI/CD pipeline triggers
 */

/**
 * Commit and push Terraform files with safety checks
 */
async function commitAndPushTerraform(repoPath, commitMessage = null, options = {}) {
  const {
    dryRun = false,
    validateFirst = true,
    autoStage = true,
    force = false
  } = options;

  console.log('[CI/CD] Starting Terraform commit and push process...');

  try {
    // 1. Validate repository operations first
    if (validateFirst) {
      console.log('[CI/CD] Validating repository operations...');
      const validation = await validateRepoOperations(repoPath);
      if (!validation.passed) {
        throw new Error(`Repository validation failed: ${validation.errors.join(', ')}`);
      }
      console.log('[CI/CD] ✅ Repository validation passed');
    }

    // 2. Check for Terraform files
    const terraformFiles = ['generated.main.tf', 'main.tf'].filter(file => 
      fs.existsSync(path.join(repoPath, file))
    );

    if (terraformFiles.length === 0) {
      throw new Error('No Terraform files found to commit (generated.main.tf, main.tf)');
    }

    console.log(`[CI/CD] Found Terraform files: ${terraformFiles.join(', ')}`);

    // 3. Generate commit message if not provided
    if (!commitMessage) {
      const timestamp = new Date().toISOString().split('T')[0];
      commitMessage = `Automated Terraform update by CloudArchitectAgent - ${timestamp}`;
    }

    // 4. Stage files
    if (autoStage) {
      console.log('[CI/CD] Staging Terraform files...');
      terraformFiles.forEach(file => {
        if (dryRun) {
          console.log(`[CI/CD] [DRY-RUN] Would stage: ${file}`);
        } else {
          execSync(`git add "${file}"`, { cwd: repoPath, stdio: 'pipe' });
          console.log(`[CI/CD] ✅ Staged: ${file}`);
        }
      });
    }

    // 5. Check if there are changes to commit
    if (!dryRun) {
      const status = execSync('git status --porcelain', { cwd: repoPath, stdio: 'pipe' }).toString();
      const stagedChanges = status.split('\n').filter(line => line.startsWith('A ') || line.startsWith('M ')).length;
      
      if (stagedChanges === 0) {
        console.log('[CI/CD] ⚠️ No changes to commit');
        return { success: false, reason: 'no_changes', message: 'No changes to commit' };
      }
      
      console.log(`[CI/CD] ${stagedChanges} changes ready to commit`);
    }

    // 6. Commit changes
    console.log('[CI/CD] Committing changes...');
    if (dryRun) {
      console.log(`[CI/CD] [DRY-RUN] Would commit with message: "${commitMessage}"`);
    } else {
      execSync(`git commit -m "${commitMessage}"`, { cwd: repoPath, stdio: 'pipe' });
      console.log('[CI/CD] ✅ Changes committed successfully');
    }

    // 7. Push to remote
    console.log('[CI/CD] Pushing to remote...');
    if (dryRun) {
      console.log('[CI/CD] [DRY-RUN] Would push to remote');
    } else {
      const pushCommand = force ? 'git push --force-with-lease' : 'git push';
      execSync(pushCommand, { cwd: repoPath, stdio: 'pipe' });
      console.log('[CI/CD] ✅ Terraform files committed and pushed successfully');
    }

    return {
      success: true,
      commitMessage,
      files: terraformFiles,
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    console.error('[CI/CD] ❌ Failed to push Terraform changes:', error.message);
    return {
      success: false,
      error: error.message,
      timestamp: new Date().toISOString()
    };
  }
}

/**
 * Enhanced commit function with conflict resolution
 */
async function smartCommitAndPush(repoPath, files, commitMessage, options = {}) {
  const {
    handleConflicts = true,
    maxRetries = 3,
    pullBeforePush = true
  } = options;

  console.log('[CI/CD] Starting smart commit and push...');

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      console.log(`[CI/CD] Attempt ${attempt}/${maxRetries}`);

      // Pull latest changes if requested
      if (pullBeforePush) {
        console.log('[CI/CD] Pulling latest changes...');
        execSync('git pull --rebase', { cwd: repoPath, stdio: 'pipe' });
      }

      // Stage specific files
      files.forEach(file => {
        if (fs.existsSync(path.join(repoPath, file))) {
          execSync(`git add "${file}"`, { cwd: repoPath });
          console.log(`[CI/CD] ✅ Staged: ${file}`);
        }
      });

      // Commit and push
      execSync(`git commit -m "${commitMessage}"`, { cwd: repoPath, stdio: 'pipe' });
      execSync('git push', { cwd: repoPath, stdio: 'pipe' });

      console.log('[CI/CD] ✅ Smart commit and push completed successfully');
      return { success: true, attempt };

    } catch (error) {
      console.warn(`[CI/CD] Attempt ${attempt} failed:`, error.message);

      if (attempt === maxRetries) {
        throw error;
      }

      // Handle common conflicts
      if (handleConflicts) {
        if (error.message.includes('conflict') || error.message.includes('merge')) {
          console.log('[CI/CD] Conflict detected, attempting resolution...');
          await resolveCommonConflicts(repoPath);
        }
      }

      // Wait before retry
      await new Promise(resolve => setTimeout(resolve, 2000 * attempt));
    }
  }
}

/**
 * Resolve common git conflicts automatically
 */
async function resolveCommonConflicts(repoPath) {
  try {
    console.log('[CI/CD] Attempting automatic conflict resolution...');

    // Get list of conflicted files
    const status = execSync('git status --porcelain', { cwd: repoPath, stdio: 'pipe' }).toString();
    const conflictedFiles = status.split('\n')
      .filter(line => line.startsWith('UU ') || line.startsWith('AA '))
      .map(line => line.substring(3).trim());

    if (conflictedFiles.length === 0) {
      console.log('[CI/CD] No conflicts detected');
      return;
    }

    console.log(`[CI/CD] Found ${conflictedFiles.length} conflicted files`);

    // For Terraform files, prefer our version (generated content)
    for (const file of conflictedFiles) {
      if (file.endsWith('.tf')) {
        console.log(`[CI/CD] Resolving Terraform conflict in ${file} (using our version)`);
        execSync(`git checkout --ours "${file}"`, { cwd: repoPath });
        execSync(`git add "${file}"`, { cwd: repoPath });
      }
    }

    console.log('[CI/CD] ✅ Conflicts resolved automatically');

  } catch (error) {
    console.error('[CI/CD] ❌ Automatic conflict resolution failed:', error.message);
    throw error;
  }
}

/**
 * Check CI/CD pipeline status
 */
async function checkPipelineStatus(repoPath, branch = null) {
  try {
    console.log('[CI/CD] Checking pipeline status...');

    // Get current branch if not specified
    if (!branch) {
      branch = execSync('git rev-parse --abbrev-ref HEAD', { cwd: repoPath, stdio: 'pipe' })
        .toString().trim();
    }

    // Get latest commit hash
    const commitHash = execSync('git rev-parse HEAD', { cwd: repoPath, stdio: 'pipe' })
      .toString().trim();

    // Check for GitHub Actions workflow files
    const workflowsDir = path.join(repoPath, '.github', 'workflows');
    const workflowFiles = fs.existsSync(workflowsDir) 
      ? fs.readdirSync(workflowsDir).filter(f => f.endsWith('.yml') || f.endsWith('.yaml'))
      : [];

    console.log(`[CI/CD] Current branch: ${branch}`);
    console.log(`[CI/CD] Latest commit: ${commitHash.substring(0, 8)}`);
    console.log(`[CI/CD] Found ${workflowFiles.length} workflow file(s): ${workflowFiles.join(', ')}`);

    return {
      branch,
      commitHash,
      workflowFiles,
      timestamp: new Date().toISOString()
    };

  } catch (error) {
    console.error('[CI/CD] ❌ Failed to check pipeline status:', error.message);
    return { error: error.message };
  }
}

/**
 * Trigger manual pipeline run (if supported)
 */
async function triggerPipeline(repoPath, workflowName = null) {
  try {
    console.log('[CI/CD] Attempting to trigger pipeline...');

    // Check if gh CLI is available
    try {
      execSync('gh --version', { stdio: 'ignore' });
    } catch {
      console.warn('[CI/CD] GitHub CLI (gh) not available, cannot trigger pipeline manually');
      return { success: false, reason: 'gh_cli_not_available' };
    }

    // Get workflow files
    const status = await checkPipelineStatus(repoPath);
    if (status.error) {
      throw new Error(status.error);
    }

    // Trigger workflow if specific name provided
    if (workflowName) {
      console.log(`[CI/CD] Triggering workflow: ${workflowName}`);
      execSync(`gh workflow run "${workflowName}"`, { cwd: repoPath, stdio: 'pipe' });
      console.log('[CI/CD] ✅ Pipeline triggered successfully');
      return { success: true, workflow: workflowName };
    } else {
      console.log('[CI/CD] No specific workflow specified');
      return { success: false, reason: 'no_workflow_specified', availableWorkflows: status.workflowFiles };
    }

  } catch (error) {
    console.error('[CI/CD] ❌ Failed to trigger pipeline:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * Monitor CI/CD pipeline execution
 */
async function monitorPipeline(repoPath, timeoutMs = 300000) { // 5 minute timeout
  try {
    console.log('[CI/CD] Monitoring pipeline execution...');
    
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeoutMs) {
      try {
        const runStatus = execSync('gh run list --limit 1 --json status,conclusion', 
          { cwd: repoPath, stdio: 'pipe' }).toString();
        
        const runs = JSON.parse(runStatus);
        if (runs.length > 0) {
          const latestRun = runs[0];
          console.log(`[CI/CD] Latest run status: ${latestRun.status}, conclusion: ${latestRun.conclusion || 'pending'}`);
          
          if (latestRun.status === 'completed') {
            return {
              completed: true,
              success: latestRun.conclusion === 'success',
              conclusion: latestRun.conclusion
            };
          }
        }
      } catch (err) {
        console.warn('[CI/CD] Unable to check run status:', err.message);
      }
      
      // Wait before next check
      await new Promise(resolve => setTimeout(resolve, 10000)); // 10 second intervals
    }
    
    return { completed: false, timeout: true };

  } catch (error) {
    console.error('[CI/CD] ❌ Pipeline monitoring failed:', error.message);
    return { completed: false, error: error.message };
  }
}

module.exports = {
  commitAndPushTerraform,
  smartCommitAndPush,
  resolveCommonConflicts,
  checkPipelineStatus,
  triggerPipeline,
  monitorPipeline
};