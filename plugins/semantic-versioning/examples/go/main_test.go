package main
import "testing"
func TestDevelopmentVersion(t *testing.T) { if version == "" { t.Fatal("version must be present") } }
