from dependencies import *

ui.label('hello world')

ui.run(title='App Deployer',host='0.0.0.0', port=8080, reload=True, native=True ,storage_secret="asdf"  )