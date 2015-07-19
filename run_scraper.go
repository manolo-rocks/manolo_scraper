package main

import (
        "fmt"
        "os/exec"
        "os"
        "bytes"
        "time"
        "strings"
        "runtime/debug"
)


func printError(err error) {
  if err != nil {
    os.Stderr.WriteString(fmt.Sprintf("==> Error: %s\n", err.Error()))
  }
}

func printOutput(outs []byte) {
  if len(outs) > 0 {
    fmt.Printf("==> Output: %s\n", string(outs))
  }
}


func main() {
    debug.PrintStack()
    baseTime := time.Now()
    t := baseTime.Add(-24*7*time.Hour)
    d := t.String()
    lastWeek := strings.Split(d, " ")[0]

    os.Chdir("/data2/ani/projects/aniversario_peru_github/manolo_scraper/manolo_scraper")

    cmdName := "tsocks"
    args1 := []string{"/home/ani/.virtualenvs/manolo_scraper/bin/scrapy", "crawl", "inpe", "-a", "date_start=%s", lastWeek}
    // args2 := []string{">", "/home/ani/Desktop/log"}
    fmt.Printf(string(args1))
    cmd := exec.Command(cmdName, args1...)
    cmdOutput := &bytes.Buffer{}
    cmd.Stdout = cmdOutput

    err := cmd.Run()
    printError(err)
    printOutput(cmdOutput.Bytes())
}
