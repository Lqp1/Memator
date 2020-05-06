# Quick howto
1. Ensure you use at least python3.6
2. Generate your reddit token for your account
3. Generate your discord token and create a bot
4. Copy `config.template.json` as `config.json` and fill the creds
5. Install env: `python3.6 -m venv env && . env/bin/activate && pip3 install -r requirements.txt`
6. Create a multi in your reddit account, and set the name in the config file.
7. Run it: `python3.6 memator.py`

# Docker howto
If you don't have a recent version of python, you can still user Docker to run
this app.
1. Generate the conf as described above
2. `docker build -t memator .`
3. `docker run -it memator`

# To be improved
- [x] OOP
- [ ] Error catching
- [ ] Add slack output
- [ ] Add local output
- [ ] Add more input feeds
- [x] Add auto send memes at fixed hour
- [ ] Filter to get only images links
