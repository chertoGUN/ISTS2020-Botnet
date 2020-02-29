package callback

type CommandRequest struct {
	Team string `json:"team,omitempty"`
	IP   string `json:"ip,omitempty"`
	User string `json:"user,omitempty"`
}

type CommandResultsRequest struct {
	ID      string `json:"id,omitempty"`
	Results string `json:"results,omitempty"`
}
