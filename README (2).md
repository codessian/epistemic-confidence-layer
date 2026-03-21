## Backend Provider Switch

This repo supports switching adapter backends between development (`UNSIGNED-DEV`) and production (`PROD`) environments.

**How it works:**
- Each adapter in `Upgrade.json` includes a `backendProviderSwitch` array (e.g., `[ "UNSIGNED-DEV", "PROD" ]`).
- The backend used depends on an environment variable, config file, or flag (see below).
- Adapters route requests to dev mocks or live endpoints based on the selected backend.

**How to switch providers:**
1. _Environment variable_:  
   Set `ECL_BACKEND_PROVIDER=PROD` or `ECL_BACKEND_PROVIDER=UNSIGNED-DEV` before starting the service.
2. _Config file_:  
   Edit the backend provider setting in `config/ecl.config.json`:
   ```json
   {
     "backendProvider": "PROD"
   }
   ```
3. _Runtime flag_ (if supported):  
   Use `--backendProvider=PROD` or `--backendProvider=UNSIGNED-DEV` when launching.

**Adapter behavior:**
- `UNSIGNED-DEV` uses mock APIs and permissive endpoints for testing.
- `PROD` uses signed requests and connects to secured, production-grade services.

**Note:**  
Provider switching is documented for each adapter in their respective code/docs. For new adapters, add `"backendProviderSwitch": [ "UNSIGNED-DEV", "PROD" ]` in `Upgrade.json` and document any custom logic here.
