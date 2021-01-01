# General Rule

General rule for response codes in NAM is:

- For all successful events, but does not need any return, return 0.

- For all successful events, or partially successful event, return a positive integer to inform the client.

- For all unsuccessful events, return a negative integer.
  
## Warnings (1 to 10)

### 101

Already following.

### 102

Already not following

### 103

Already pinned

### 104

Already unpinned

### 10000

Development Mode

## -1 to -10 Family

Common Errors that may arise.

### -1

Request has failed, with no explanation or explanation in message.

## -100 Family

Authentication issue

### -101

Authentication can not be completed as no login request was initiated.

### -102

The OTP has expired.

### -103

Incorrect OTP

### -104

Maximum attempts reached. Please request another OTP.

### -105

User not registered.

### -106

User already registered.

### -107

Authentication required.

### -108

Invalid token

### -109

Token has expired

### -110

Unknown scope

### -111

Insufficient permission: missing permission.

### -112

uuid may not be updated

### -113

Properties validation failed

### -114

Could not commit changes to the database

## -10000 Family

Error Related to Args Module

### -10001

An argument of a function was not supplied.

### -10002

The argument supplied is invalid or could not be converted to the expected format. (When convertion function raises an exception)

### -99999

Internal Server Error
