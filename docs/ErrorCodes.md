# General Rule

General rule for response codes in Groups is:

- For all successful events, but does not need any return, return 0.

- For all successful events, or partially successful event, return a positive integer to inform the client.

- For all unsuccessful events, return a negative integer.
  
## Warnings (1 to 10)

### 10000

Development Mode

## -1 to -10 Family

Common Errors that may arise.

### -1

Request has failed, with no explanation or explanation in message.

## -10000 Family

Error Related to Args Module

### -10001

An argument of a function was not supplied.

### -10002

The argument supplied is invalid or could not be converted to the expected format. (When convertion function raises an exception)