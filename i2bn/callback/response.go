package callback

type Response struct {
	Command string      `json:"command"`
	ID      string      `json:"id"`
	IP      string      `json:"ip"`
	Team    string      `json:"team"`
	Type    string      `json:"type"`
	User    string      `json:"user"`
	Error   string      `json:"error"`
	Msg     string      `json:"msg"`
	Time    interface{} `json:"time"`
}

func (r *Response) IsError() bool {
	return r.Error != ""
}
