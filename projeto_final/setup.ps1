# Caminho da pasta local com os dados do PostgreSQL
$hostPath = "C:\Users\eufil\dados_postgresql"
$minikubePath = "/mnt/postgresdata"

#kubectl delete all --all


Write-Host "`n🔄 Iniciando o Minikube e dependencias..."
minikube start
minikube addons enable metrics-server


& minikube -p minikube docker-env | Invoke-Expression
docker build -t projeto_final_asa:03 .\app
Start-Process -FilePath "powershell" -ArgumentList 'minikube mount "C:\Users\eufil\dados_postgresql:/mnt/postgresdata"' -WindowStyle Normal



kubectl apply -f ./k8s/

Start-Sleep -Seconds 5

Start-Process -FilePath "powershell" -ArgumentList 'kubectl port-forward service/projeto-asa-service 80:8000' -WindowStyle Normal
Start-Process -FilePath "powershell" -ArgumentList 'kubectl port-forward service/postgres 5432:5432' -WindowStyle Normal


#Write-Host "`n✅ Tudo pronto! Use 'kubectl get pods' para verificar os pods e 'kubectl port-forward service/minha-app-service 80:80' para acesso local."
