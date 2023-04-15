# Invoke Xircuits Components

Component library for invoking other .xircuits files.

![invoke](https://github.com/XpressAI/xai-invoke-xircuits/blob/main/invoke.png)

![output](https://github.com/XpressAI/xai-invoke-xircuits/blob/main/output.png)

## Components

- InvokeXircuitsFile
  Compile and run another xircuits file.  Any `Arguments` the
  target Xircuits file needs must be provided in the `in_args`
  dictionary.

- XircuitOutput
  Add a value to be included in the final output of this 
  Xircuits.  Will be picked up by `InvokeXircuitsFile` and
  available as the `outputs` dictionary.

- SetDictValue
  Add a value to the provided dictionary (or new dictionary
  if none provided.)

- GetDictValue
  Gets the value from a dictionary.

## Roadmap

This component library will eventually be included into a 
future Xircuits release.

