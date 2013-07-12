from service import app
import sys

if len(sys.argv) != 2:
	print "usage: python start_service.py <option:prod or dev>"
else:
	if sys.argv[1] == "dev":
		app.run(debug=True)
	elif sys.argv[1] == "prod":
		app.run(debug=False)
	else:
		print "wrong option: " + sys.argv[1] 
