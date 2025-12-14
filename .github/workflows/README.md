# GitHub Actions Workflows

## Build and Test Workflow

The `build.yml` workflow runs automatically on every push to `main` and on pull requests.

### What It Does

1. **Type Safety Checks**
   - Runs `pyright` on source code
   - Runs `pyright` on solutions
   - Ensures all code is type-safe

2. **Django Checks**
   - Runs `check --deploy` to verify production readiness
   - Checks for missing migrations
   - Validates migration integrity
   - Tests static file collection

3. **Build Validation**
   - Verifies `build.sh` syntax
   - Confirms gunicorn is available
   - Ensures all dependencies install correctly

### Workflow

```
Push to main
    ↓
GitHub Actions runs tests
    ↓
✅ All checks pass
    ↓
Render.com detects push
    ↓
Render builds & deploys automatically
```

### If Build Fails

GitHub Actions will fail and show you which check failed. Fix the issue before Render attempts to deploy.

### Viewing Results

Go to your repository → **Actions** tab to see:
- ✅ Passing builds (green checkmark)
- ❌ Failed builds (red X)
- Detailed logs for each step

### Local Testing

Run the same checks locally before pushing:

```bash
# Type checks
uv run pyright src
uv run pyright solutions

# Django checks
uv run python src/aoc2025/web/manage.py check --deploy

# Static files
uv run python src/aoc2025/web/manage.py collectstatic --noinput

# Build script
bash -n build.sh
```

### Caching

The workflow caches dependencies to speed up builds:
- First build: ~2-3 minutes
- Cached builds: ~1-2 minutes

### Secrets Management

The workflow automatically generates a secure secret key for testing. If you need to add other secrets:

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add your secret (e.g., `API_KEY`)

Then use it in the workflow:

```yaml
- name: Run with secret
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    echo "Secret is available but not printed"
```

**Current secrets used:**
- `DJANGO_SECRET_KEY` - Auto-generated per build (not stored)

### Adding More Checks

To add more checks, edit `.github/workflows/build.yml` and add steps like:

```yaml
- name: Run tests
  run: |
    uv run pytest
```

## Best Practices

1. **Always check locally first** before pushing
2. **Fix failing builds immediately** - don't ignore them
3. **Review the logs** if a build fails to understand why
4. **Keep builds fast** - they run on every push

## Status Badge

Add to your README.md:

```markdown
![Build Status](https://github.com/yourusername/aoc2025/workflows/Build%20and%20Test/badge.svg)
```
