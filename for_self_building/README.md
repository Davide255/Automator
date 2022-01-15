# Self-Building dipendences

- Install requirements by <code>pip install -r requirements.txt</code> 
- Move the <code>Automator.spec</code> file in the main directory where <code>Automator.py</code> file sits.
- Start building by <code>python -m pyinstaller ./Automator.spec</code>
- The output will be <code>./dist/Automator.exe</code>

# Building errors

- [CRITICAL] [Camera      ] Unable to find any valuable Camera provider. Please enable debug logging (e.g. add -d if running from the command line, or change the log level in the config) and re-run your app to identify potential causes

Skip this error, camera isn't envolved in Automator

# exe errors

- [CRITICAL] [Window      ] Unable to find any valuable Window provider. Please enable debug logging (e.g. add -d if running from the command line, or change the log level in the config) and re-run your app to identify potential causes
sdl2 - Exception: SDL2: Unable to load image

Add those 3 lines at the top of Automator.py file:
```python
os.environ['KIVY_IMAGE'] = "pil,sdl2"
os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\glew\\bin')
os.environ['PATH'] += ';' + os.path.expandvars('%AppData%\\Python\\share\\sdl2\\bin')
```
Now re-build using the Automator.spec file
