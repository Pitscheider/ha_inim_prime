## Introduction
inim_prime_api allows you to communicate with INIM Prime alarm panels over HTTP/HTTPS using an asynchronous API with
Python.
An Inim PrimeLAN card is needed in order to communicate.
## Development process
I created this package cause I needed a client to communicate with an Inim Prime panel in order to create an Home Assistant integration.
I am not an Inim installer, and i tested and developed the client based on my panel only (which is an italian one) and using the API documentation i found online.
You can check the documentation there: PrimeLAN Web API documentation. 
I tried to implement the API using a panel with the firmware 4.07.
The client code maps responses and requests to models I accurately created for each entity of the Inim Prime panel.
Here is a list of the functions that are currently implemented:
- Get API version
- Ping
- Get zones status
- Get outputs status
- Get partitions status
- Get scenarios status
- Get log events
- Get GSM status
- Get system faults status (I haven't checked if all the possible faults are mapped correctly, but I tried my best to do so. In case you find a situation in which it does not work, please open an issue).
- Set zone exclusion
- Set output
- Set partition mode
- Clear partition alarm memory
- Activate scenario

I have to specify that not all of the above functions do really work on my panel. 
I had problems with:
- Get output zones, in fact the list returned is empty even though it should be returning a few outputs. That function worked with the previous firmware and is a problem of the panel API that cannot be fixed by me.
- Set output, in fact it does not actually changes the output. That function worked with the previous firmware and is a problem of the panel API that cannot be fixed by me.
- Activate scenario, in fact in my setup it does not actually activate the scenario. In Prime/STUDIO I tried to create the link that should work, but it hasn't activated anything either. I believe it is also a problem of the panel API, that cannot be fixed by me.

Moreover, I have not been able to implement those features, since they return an error and have to be fixed by Inim:
- Get list of open zones of a given partition
- Get list of open zones of a given scenario
## Development env
I developed the whole client using PyCharm Community.
## Try the client
To try this client you can use the interactive python script that I have included in test. To save the credentials, just create a file in the root of the repo called .env:
```
INIM_HOST = "host address (like 192.168.1.2)"
INIM_API_KEY = "api_key"
```

## License
This project is licensed under GNU GPL v3.

made with ❤️ by Pitscheider