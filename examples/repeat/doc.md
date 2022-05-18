# Repeat

## Examples
```xml
<repeat var="i" range="0;100;10">
    <rect x="{i}" y="0" width="5" height="5" />
</repeat>
```

<br>

## Parameters

### var
The name of the counter variable which will be used. (The same name can't be used nested)

<br>

### range
The range of the counter. The counter will be incremented by the step size.

<br>

**Schema:**
`<start>;<stop>;<step>`

**start:** The number the counter will start at.

**end:** The number the counter will stop at.

**step:** The number the counter will increment by.

<br>

If `end > start` the step size must be negative too.