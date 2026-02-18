package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strings"

	"github.com/common-nighthawk/go-figure"
	"github.com/pterm/pterm"
	"gopkg.in/yaml.v3"
)

type TokenMessage struct {
	Type string `json:"type"`
	Text string `json:"text"`
}

type Config struct {
	ServerURL string `yaml:"server_url"`
}

var spinner *pterm.SpinnerPrinter

func loadConfig(path string) Config {
	cfg := Config{
		ServerURL: "http://localhost:8000",
	}

	data, err := os.ReadFile(path)
	if err != nil {
		pterm.Warning.Println("Config file not found, using defaults")
		return cfg
	}

	err = yaml.Unmarshal(data, &cfg)
	if err != nil {
		pterm.Warning.Println("Error parsing config, using defaults:", err)
		return cfg
	}

	return cfg
}
func exeDir() string {
	ex, err := os.Executable()
	if err != nil {
		log.Fatal(err)
	}
	return filepath.Dir(ex)
}
func main() {

	if len(os.Args) < 2 {
		pterm.Info.Println("Usage: verity.exe \"your question\"")
		return
	}
	configPath := filepath.Join(exeDir(), "config.yaml")
	cfg := loadConfig(configPath)

	query := os.Args[1]
	encoded := url.QueryEscape(query)

	endpoint := fmt.Sprintf("%s/ask?question=%s&return_src_md=false", cfg.ServerURL, encoded)

	req, err := http.NewRequest("GET", endpoint, nil)
	if err != nil {
		pterm.Error.Println("Request creation failed: %v", err)
		os.Exit(1)
	}

	req.Header.Set("Accept", "text/event-stream")

	client := &http.Client{Timeout: 0}

	resp, err := client.Do(req)
	if err != nil {

		pterm.Error.Println("❌ Unable to connect to Verity backend: %v", err)
		pterm.Warning.Printfln("Ensure Verity webserver is running.")
		os.Exit(1)
	}
	defer resp.Body.Close()

	//fmt.Println("Verity")
	myFigure := figure.NewColorFigure("Verity", "", "green", true)
	myFigure.Print()
	blueStyle := pterm.NewStyle(pterm.FgGreen)
	blueStyle.Println("✨ Answer :")

	reader := bufio.NewReader(resp.Body)

	var currentEvent string

	for {
		line, err := reader.ReadString('\n')
		if err != nil {
			break
		}

		line = strings.TrimRight(line, "\n")

		if strings.HasPrefix(line, "event:") {
			currentEvent = strings.TrimSpace(strings.TrimPrefix(line, "event:"))
			continue
		}

		if strings.HasPrefix(line, "data:") {

			data := strings.TrimPrefix(line, "data:")
			data = strings.TrimSpace(data)

			if data == "" || data == "[DONE]" {
				continue
			}

			handleEvent(currentEvent, data)
		}
	}
}

func handleEvent(event string, data string) {

	switch event {

	case "search":
		startSpinner("🔍 Searching...")

	case "read":
		startSpinner("📖 Reading...")

	case "think":
		startSpinner("🧠 Preparing answer...")

	case "error":
		fmt.Println("\n")
		pterm.Error.Println("Error:", data)

	case "token":
		stopSpinner()

		var msg TokenMessage
		if err := json.Unmarshal([]byte(data), &msg); err == nil {
			fmt.Print(msg.Text)
		}

	case "done":
		stopSpinner()
	}
}

func startSpinner(message string) {

	stopSpinner()

	var err error
	spinner, err = pterm.DefaultSpinner.
		WithRemoveWhenDone(true).
		WithSequence("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏").
		Start(message)
	if err != nil {
		panic(err)
	}
}

func stopSpinner() {
	if spinner != nil {
		spinner.Stop()
		spinner = nil
	}
}
