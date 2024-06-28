Based on the search results and the context provided, here's a guide on how to resolve the "pipx command not found" issue and properly use pipx:

1. Install pipx:
   If pipx is not recognized, you need to install it first. You can do this using pip:

   ```
   python3 -m pip install --user pipx
   ```

2. Add pipx to PATH:
   After installation, you need to ensure pipx is in your system's PATH. Run:

   ```
   python3 -m pipx ensurepath
   ```

   If this doesn't work, you may need to add it manually:

   ```
   export PATH="${PATH}:$(python3 -c 'import site; print(site.USER_BASE)')/bin"
   ```

3. Restart your terminal:
   Close and reopen your terminal or command prompt for the PATH changes to take effect.

4. Verify installation:
   Check if pipx is now recognized:

   ```
   pipx --version
   ```

5. If still not found:
   - On Windows, you might need to run `.\pipx.exe ensurepath` from the installation directory.
   - On macOS, you can install pipx using Homebrew: `brew install pipx`
   - On Linux, you can use your distribution's package manager or pip.

6. Use pipx:
   Once properly installed, you can use pipx to install Python applications in isolated environments:

   ```
   pipx install package_name
   ```

7. Global installation (optional):
   If you want to allow pipx actions in global scope:

   ```
   sudo pipx ensurepath --global
   ```

Remember, pipx is designed to install and run Python applications in isolated environments, which is different from installing Python packages for development. If you're trying to use a Python package in your code, you might need to install it using pip instead of pipx.

If you continue to have issues, make sure your Python installation is correct and that you're using the intended version of Python when installing and running pipx.

