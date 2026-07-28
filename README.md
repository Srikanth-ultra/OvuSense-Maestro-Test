# OvuSense Maestro UI Tests

Automated UI test suite for the **OvuSense 3.2.0** Android app using [Maestro](https://maestro.mobile.dev/). Covers settings, data, logs, help, and account flows across 10 test accounts with different feature sets.

## Project Structure

```
flows/
├── 01–41_*.yaml          # 41 top-level test flows
├── bodies/               # 29 detailed test step files
├── helpers/              # 6 reusable login/logout utilities
└── chains/               # 5 chained multi-flow sessions
config/
└── accounts.env          # Test account credentials and flow mapping
.github/workflows/
└── maestro-tests.yml     # CI pipeline (4 parallel shards)
dashboard.html            # Test results dashboard
```

## Test Coverage

| Area | Flows |
|------|-------|
| Settings (account, preferences, sensors, notifications, data sharing) | 01, 09, 13, 24–29, 39 |
| Help & User Guide | 02, 38 |
| Me Tab | 03, 12, 37 |
| Data Tab (graphs, cycles, pods, day events, shared user) | 04, 06, 07, 30–33, 35 |
| Logs (selection, reorder, mood, diet, exercise, medication, temperature) | 08, 14, 18–23 |
| Login / Logout / Onboarding | 05, 34, 36 |
| Special Accounts (preg, high, free, nosub, none, oldsensor) | 10, 15, 23 |
| Updates & Bug Fixes | 11, 17, 40 |
| Pods | 16 |

## Test Accounts

All accounts use the password `ovutest?0`:

| Account | Purpose | Flows |
|---------|---------|-------|
| test@ovusense.com | Default / general testing | 01–04, 07–09, 11–12, 14, 18–22, 24, 26–29, 33, 37–39, 41 |
| pods@ovusense.com | Pod-enabled features | 06, 13, 16, 25, 30–32 |
| lots@ovusense.com | Large dataset / many cycles | 05, 34 |
| rnd26@ovusense.com | RnD26 graph marker features | 17, 40 |
| preg@ovusense.com | Pregnancy/health features | 10, 35 |
| none@ovusense.com | No sensor account | 15, 23 |
| oldsensor@ovusense.com | Legacy sensor account | 15, 23 |
| nosub@ovusense.com | No subscription | 10, 23 |
| high@ovusense.com | High-risk account | 10 |
| free@ovusense.com | Free tier account | 10 |

## Prerequisites

- [Maestro CLI](https://maestro.mobile.dev/) installed
- Android device or emulator connected via ADB
- OvuSense 3.2.0 debug APK installed

## Running Tests

Run a single flow:

```bash
maestro test flows/01_settings_tab.yaml
```

Run a chain (multiple flows in one login session):

```bash
maestro test flows/chains/chain_test_A.yaml
```

Run all flows:

```bash
for f in flows/[0-9]*.yaml; do maestro test "$f"; done
```

## How It Works

- **Flows** are the top-level entry points — each launches the app and delegates to a body file or runs inline steps.
- **Bodies** contain the detailed UI interactions, assertions, and screenshot captures. They reference test case IDs (e.g., TC-140, TC-141).
- **Helpers** provide reusable login/logout logic, accepting `EMAIL` and `PASSWORD` as environment variables.
- **Chains** group multiple body files under a single login session for faster execution.

## CI / GitHub Actions

The workflow (`.github/workflows/maestro-tests.yml`) runs on push to `main`/`develop` and on pull requests.

### Manual Dispatch Options

Trigger the workflow manually from the **Actions** tab with these inputs:

| Input | Description | Options |
|-------|-------------|---------|
| **test_scope** | What to run | `all` (default), `feature`, `flows` |
| **feature** | Feature area (when scope = `feature`) | `settings`, `help`, `me_tab`, `data_tab`, `logs`, `login_onboarding`, `special_accounts`, `updates_bugfixes`, `pods` |
| **flows** | Comma-separated flow numbers (when scope = `flows`) | e.g. `01,05,10` |
| **shard_count** | Parallel shards | `1`–`4` (default: `4`) |
| **api_level** | Android emulator API level | `30`, `31`, `33`, `34` (default: `33`) |
| **apk_url** | Custom APK download URL | blank = default dev APK |

### Feature-to-Flow Mapping

| Feature | Flows |
|---------|-------|
| `settings` | 01, 09, 13, 24, 25, 26, 27, 28, 29, 39 |
| `help` | 02, 38 |
| `me_tab` | 03, 12, 37 |
| `data_tab` | 04, 06, 07, 30, 31, 32, 33, 35 |
| `logs` | 08, 14, 18, 19, 20, 21, 22, 23 |
| `login_onboarding` | 05, 34, 36 |
| `special_accounts` | 10, 15 |
| `updates_bugfixes` | 11, 17, 40 |
| `pods` | 16 |

### Examples

Run only settings tests:
> Actions → Run workflow → test_scope: `feature`, feature: `settings`

Run specific flows 01, 05, and 10:
> Actions → Run workflow → test_scope: `flows`, flows: `01,05,10`

Run everything (default on push/PR):
> Actions → Run workflow → test_scope: `all`
