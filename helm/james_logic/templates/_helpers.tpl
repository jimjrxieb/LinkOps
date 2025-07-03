{{- define "james-logic.serviceAccountName" -}}
{{ .Values.serviceAccount.name | default (printf "%s-sa" .Chart.Name) }}
{{- end }}

{{- define "james-logic.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }} 