# For

## Examples

```xml
<for i="range(0, 10)">
    <rect x="{i*10}" y="0" width="5" height="5" />
</for>
```

```xml
<for i="0; i smaller 10; i+=1">
    <rect x="{i*10}" y="0" width="5" height="5" />
</for>
```

<br>

## Parameters

### any

**Name** <br>

The name of the counter variable which will be used (Use _ to specify not using a variable).

**Value** <br>

***Range*** <br>
An expression that returns a python range object. <br>

***C like for expression*** <br>
`<start>;<cond>;<after>`<br