A way to automate contacting businesses who already gave implicit consent via contact form. Only contacting them through contact methods provided/published publically via contact form. Still under construction.



To use the chrome extension:



1. Add the chrome extension from the source using the folder: 

> chrome-extension/



2. start server:

> python3 -m pip install -r requirements.txt <br/>
> python3 run.py <br/>
> go to http://0.0.0.0:5003/upload

3. Upload JSON generated from the chrome extention

4. Go to http://0.0.0.0:5003/sql_dump

5. Copy and paste the page content and import into MailChimp



