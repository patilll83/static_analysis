## Deliverable 3: Reflection Questions

Here are the reflections on the lab experience.

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

* **Easiest:** The `eval()` use (flagged by Bandit) was the easiest. The fix was simply to delete the line, as it served no functional purpose. The broad `except:` was also easy; it was a clear-cut replacement of `except:` with `except KeyError:`.
* **Hardest:** The `dangerous-default-value` (`logs=[]`) was the most conceptually difficult. It's not an obvious syntax error, but a subtle bug related to how Python initializes function defaults only *once*. The *best* fix involved a minor refactor to remove the parameter and use the `logging` module properly, which was more involved than a simple one-line change.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

* Yes, `pylint` in particular can be "noisy." A common false positive it might generate is `C0103: invalid-name` for simple loop iterators (e.g., `for i in stock_data:`). While `i` could be renamed to `item`, using `i` is a widely accepted convention that doesn't harm readability, but Pylint often flags it.

**3. How would you integrate static analysis tools into your actual software development workflow?**

I would integrate them in two key places:

* **Local Development (Pre-commit Hooks):** I would use a `pre-commit` hook. This script runs automatically *before* a developer is allowed to `git commit`. I would configure it to run `flake8` and `bandit`. If either tool finds a high-severity issue, the commit is automatically aborted, forcing a fix *before* it even enters the repository.
* **Continuous Integration (CI) Pipeline:** I would add a "Lint & Test" stage to the CI pipeline (e.g., in GitHub Actions). On every pull request, this job would run all three tools. `Pylint` would be configured with a minimum score threshold (e.g., 9/10). If the score is too low or `bandit` finds issues, the build fails, blocking the pull request from being merged.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

The improvements were significant:

* **Robustness:** The program is much less fragile. It no longer crashes if you try to get a non-existent item (due to `.get()`) or remove one (due to `except KeyError:`). It also handles file I/O safely and validates input types, preventing crashes from bad data.
* **Security:** The most critical `eval()` vulnerability was eliminated.
* **Readability/Maintainability:** The code is far easier to understand. All functions now have `snake_case` names (PEP 8), docstrings explaining *what* they do, and proper logging. When something goes wrong, the `logging` output provides a clear, timestamped message, which makes debugging infinitely easier than the original code's silent failures.