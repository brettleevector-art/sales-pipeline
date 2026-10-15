# Git & GitHub Lab — Sales Pipeline

**Audience:** Data engineers new to Git  **Time:** ~2.5 hours  **Needs:** Git, Python 3, a GitHub account

Each exercise has a **Goal**, the **Steps**, and a **Check** so you know you got it right.
Replace `<your-username>` with your GitHub username everywhere.

---

## Exercise 0 — One-time setup (10 min)

```bash
git --version
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --list
```

**Check:** `git config user.name` prints your name.

---

## Exercise 1 — Create your first repository (15 min)

**Goal:** Turn the project folder into a Git repo and make the first commit.

```bash
cd sales-pipeline
python pipeline.py            # creates data/processed/ and data/warehouse.db
git init
git status                    # note: processed/ and warehouse.db are NOT listed
```

> **Why aren't they listed?** Open `.gitignore`. Data engineers should commit *code and small
> sample data*, never generated outputs, databases, or secrets (`.env`).

```bash
git add .
git status                    # files are now "staged" (green)
git commit -m "Initial commit: sales ETL pipeline"
git log --oneline
```

**Check:** `git log --oneline` shows exactly one commit.

**Think:** What are the three areas? *Working directory → Staging area → Repository.*

---

## Exercise 2 — Track changes with diff (15 min)

**Goal:** See exactly what changed before committing.

1. Open `sql/reports.sql` and add a second query at the bottom:
   ```sql
   -- Top 3 customers by spend
   SELECT customer, ROUND(SUM(amount), 2) AS spend
   FROM sales GROUP BY customer ORDER BY spend DESC LIMIT 3;
   ```
2. Run:
   ```bash
   git status
   git diff                   # unstaged changes
   git add sql/reports.sql
   git diff --staged          # staged changes
   git commit -m "Add top customers report"
   ```

**Check:** `git log --oneline` shows 2 commits. `git show HEAD` displays your SQL.

---

## Exercise 3 — Undo mistakes (15 min)

**Goal:** Learn the safe "undo" buttons.

| Situation | Command |
|---|---|
| Messed up a file, not staged yet | `git restore <file>` |
| Staged by accident | `git restore --staged <file>` |
| Bad commit message (not pushed) | `git commit --amend -m "new msg"` |
| Undo a pushed commit safely | `git revert <commit-id>` |

Try it:
```bash
echo "garbage" >> etl/config.py
git diff                       # see the damage
git restore etl/config.py      # gone
git status                     # clean
```

Now simulate a bad commit and revert it:
```bash
echo "TAX_RATE = 5" >> etl/config.py
git commit -am "Oops wrong tax"
python pipeline.py             # amounts look wildly wrong
git revert HEAD --no-edit
python pipeline.py             # back to normal
git log --oneline
```

**Check:** Log shows both the "Oops" commit and a "Revert ..." commit. History is preserved — that's why `revert` is safe for shared branches.

---

## Exercise 4 — Push to GitHub (15 min)

**Goal:** Put your repo online.

1. On GitHub: **New repository** → name `sales-pipeline` → **do not** add a README/.gitignore → Create.
2. Connect and push:
   ```bash
   git remote add origin https://github.com/<your-username>/sales-pipeline.git
   git remote -v
   git push -u origin main
   ```
   (When prompted for a password, use a **Personal Access Token**, not your GitHub password —
   GitHub → Settings → Developer settings → Tokens. Or set up SSH keys.)

**Check:** Refresh GitHub. You see your files and commits. `data/warehouse.db` is **not** there.

---

## Exercise 5 — Feature branch: add a new data file (20 min)

**Goal:** Work on a branch, the way real teams do.

```bash
git switch -c feature/feb-data
```

1. Copy `sales_2026_02.csv` (given by your instructor) into `data/raw/`.
2. Run the pipeline — extract should now read **15** rows:
   ```bash
   python pipeline.py
   ```
3. Commit and push the branch:
   ```bash
   git add data/raw/sales_2026_02.csv
   git commit -m "Add February 2026 sales data"
   git push -u origin feature/feb-data
   ```
4. Switch back and notice the file disappears:
   ```bash
   git switch main
   ls data/raw                # only January!
   git switch feature/feb-data
   ls data/raw                # February is back
   ```

**Check:** `git branch -a` lists `main`, `feature/feb-data`, and `remotes/origin/feature/feb-data`.

---

## Exercise 6 — Pull Request & merge on GitHub (15 min)

**Goal:** Review and merge through GitHub.

1. On GitHub you'll see **"Compare & pull request"** → click it.
2. Title: `Add February 2026 sales data`. Description: what changed + row counts.
3. Open the **Files changed** tab and leave a comment on one line (code review!).
4. Click **Merge pull request** → **Delete branch**.
5. Back in the terminal, get the merged result:
   ```bash
   git switch main
   git pull
   git branch -d feature/feb-data
   ls data/raw                # both months now on main
   ```

**Check:** `git log --oneline --graph` shows the merge.

---

## Exercise 7 — Merge conflict! (25 min) ⚠️

**Goal:** Create and resolve a conflict — the classic scenario of two engineers changing the same setting.

```bash
# Engineer A
git switch -c change-tax-a
sed -i 's/TAX_RATE = 0.18/TAX_RATE = 0.12/' etl/config.py   # Mac: sed -i ''
git commit -am "Set tax to 12%"

# Engineer B (from main)
git switch main
git switch -c change-tax-b
sed -i 's/TAX_RATE = 0.18/TAX_RATE = 0.05/' etl/config.py
git commit -am "Set tax to 5%"

# Merge both into main
git switch main
git merge change-tax-a        # fast, no problem
git merge change-tax-b        # CONFLICT!
```

Open `etl/config.py`. You'll see:
```
<<<<<<< HEAD
TAX_RATE = 0.12
=======
TAX_RATE = 0.05
>>>>>>> change-tax-b
```

Decide the correct value (say the business confirmed 18% is right), delete the markers, leave one line:
```python
TAX_RATE = 0.18
```
Then:
```bash
python -m unittest            # always test after resolving!
git add etl/config.py
git commit -m "Resolve tax conflict: keep 18%"
git branch -d change-tax-a change-tax-b
git push
```

**Check:** No `<<<<<<<` markers remain (`grep -r "<<<<" .` returns nothing) and the pipeline runs.

---

## Exercise 8 — Collaborate with a partner: Fork & PR (20 min)

**Goal:** Contribute to someone else's repo (pair up).

1. Fork your partner's `sales-pipeline` on GitHub.
2. Clone **your fork**:
   ```bash
   git clone https://github.com/<your-username>/sales-pipeline.git partner-pipeline
   cd partner-pipeline
   git switch -c feature/region-filter
   ```
3. Add a new report to `sql/reports.sql`:
   ```sql
   -- Monthly revenue
   SELECT substr(order_date, 1, 7) AS month, ROUND(SUM(amount), 2) AS revenue
   FROM sales GROUP BY month ORDER BY month;
   ```
4. Commit, push, and open a PR **to your partner's repo**.
5. Partner reviews: request a change, then approve and merge.
6. Keep your fork in sync:
   ```bash
   git remote add upstream https://github.com/<partner-username>/sales-pipeline.git
   git fetch upstream
   git switch main
   git merge upstream/main
   ```

**Check:** Your report appears in your partner's `main` branch history with your name.

---

## Exercise 9 — Tag a release (5 min)

**Goal:** Mark a known-good version of the pipeline.

```bash
git tag -a v1.0 -m "First stable pipeline: Jan + Feb data"
git push origin v1.0
```
On GitHub: **Releases → Draft a new release** → choose `v1.0`.

**Check:** `git tag` lists `v1.0`.

---

## 🏆 Bonus challenges

1. **Secret leak drill:** Create `.env` with `DB_PASSWORD=secret`. Run `git status` — why isn't it shown?
   Now try `git add -f .env` and *don't* commit — unstage it. Discuss what to do if a secret **is** pushed (rotate it!).
2. **Stash:** Start editing `transform.py`, then get an "urgent fix" request. Use `git stash`, fix on another branch, `git stash pop`.
3. **Blame & history:** `git log -p etl/config.py` and `git blame etl/config.py` — who changed the tax rate and when?
4. **Issues:** Open a GitHub Issue "Reject negative quantities", fix it in a branch, and close it with a commit message `Fixes #1`.
5. **GitHub Actions:** Add `.github/workflows/test.yml` that runs `python -m unittest` on every push.

---

## Cheat sheet

| Task | Command |
|---|---|
| Status | `git status` |
| Stage / commit | `git add <file>` · `git commit -m "msg"` |
| History | `git log --oneline --graph --all` |
| New branch | `git switch -c <name>` |
| Change branch | `git switch <name>` |
| Merge | `git merge <branch>` |
| Push / pull | `git push` · `git pull` |
| Undo local edit | `git restore <file>` |
| Undo pushed commit | `git revert <id>` |
| Stash | `git stash` · `git stash pop` |

### Data engineering Git rules
- ✅ Commit code, SQL, configs, tests, **small** sample data
- ❌ Never commit large datasets, `.db`/`.parquet` outputs, credentials, `.env`
- 🧪 Run tests before every push and after every conflict
- 📝 One logical change per commit, clear messages
