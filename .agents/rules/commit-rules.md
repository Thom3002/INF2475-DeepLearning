# Commit Message Guidelines

Whenever you are asked to make a commit, or when you are preparing code changes that require a commit, you must follow these rules:

1. **Language**: Always write commit messages in **English**.
2. **Format**: Follow the **Conventional Commits** specification:
   `<type>(<optional scope>): <description>`
3. **Style**:
   - Keep messages **short, succinct, objective, and easy to understand**.
   - Use the **imperative mood** (e.g., "add data validation" instead of "added data validation" or "adds data validation").
   - Do not capitalize the first letter of the description.
   - Do not end the description with a period.
   - Keep the entire commit message line under 72 characters.

## Commit Types
- `feat`: A new feature.
- `fix`: A bug fix.
- `docs`: Documentation only changes.
- `style`: Changes that do not affect the meaning of the code (formatting, missing semi-colons, white space, etc.).
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `perf`: A code change that improves performance.
- `test`: Adding missing tests or correcting existing tests.
- `build`: Changes that affect the build system or external dependencies.
- `ci`: Changes to CI configuration files and scripts.
- `chore`: Other changes that do not modify `src` or `test` files.

## Example Good Commits
- `feat(api): add route for prediction model`
- `fix(models): resolve shape mismatch in training loop`
- `docs: update setup instructions in readme`
- `refactor(utils): simplify data preprocessing function`
