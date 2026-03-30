# CDP Go SDK

> **Status**: Planned for v0.2.0

The Go SDK for the Capability Discovery Protocol is under development.

## Planned Features

- `adp.Client` for discovery, registration, and federation
- Full type definitions for all CDP protocol messages
- HTTP transport with configurable timeout and retry
- Context support for cancellation

## Estimated Timeline

Go SDK is targeted for the v0.2.0 release.

## Contributing

If you'd like to contribute to the Go SDK, please open an issue on GitHub.

## Using the API Directly

Until the Go SDK is available, you can use CDP from Go via the HTTP API:

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
)

type DiscoveryIntent struct {
    IntentText string `json:"intent_text"`
    Category   string `json:"category"`
}

func main() {
    intent := DiscoveryIntent{
        IntentText: "I need noise-canceling headphones",
        Category:   "product",
    }
    body, _ := json.Marshal(intent)
    resp, err := http.Post("http://localhost:8000/discover", "application/json", bytes.NewBuffer(body))
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()
    fmt.Println("Status:", resp.Status)
}
```
