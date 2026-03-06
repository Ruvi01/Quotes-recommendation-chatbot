param(
  [switch]$Train,
  [switch]$Test,
  [switch]$Shell,
  [switch]$Serve,
  [switch]$Web
)

if ($Train) {
  rasa train
}

if ($Test) {
  rasa test
}

if ($Shell) {
  rasa shell
}

if ($Serve) {
  rasa run --enable-api --cors "*"
}

if ($Web) {
  python .\webapp\app.py
}
