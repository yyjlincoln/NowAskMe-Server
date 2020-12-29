# API Plan

## Structure

The server is structured like this:

RegisterRequest -> Handle Flask -> Handle ....

Then, when a request comes in:

Request -> Map Request (Utils) -> View (Call and Manipulate Core) -> Core (Core) -> View (Views).

This will reduce the complexity of the software and hence avoid bugs

The handler is responsible for retrieving and parsing the coming HTTP(s) request.
