{{- define "james-logic.serviceAccountName" -}}
{{ .Values.serviceAccount.name | default (printf "%s-sa" .Chart.Name) }}
{{- end }} 