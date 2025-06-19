# Projeto-TV

Este projeto é uma aplicação web desenvolvida com Python (Flask), HTML5, JavaScript e TailwindCSS, que serve como painel de monitoramento e controle de pedidos e remessas em tempo real. A aplicação lê arquivos .txt contendo informações de remessas distribuídas em diversos diretórios (checkouts), classifica os pedidos como FARMA ou HOSP com base em palavras-chave, e exibe essas informações em uma interface limpa e responsiva.

Funcionalidades principais:

Classificação automática de remessas por tipo de cliente.

Atualização dinâmica dos dados via JavaScript (fetch + setInterval).

Interface de busca por remessas nos checkouts.

Letreiro automático exibido em tela cheia com texto customizável.

Captura e envio de dados da área de transferência (clipboard) para atualização de pedidos.

Geração de relatórios de log com divisão de remessas por tipo.

Exibição direta no navegador, com abertura automática das janelas.

Tecnologias utilizadas:

Flask (backend em Python)

HTML, JavaScript, TailwindCSS para personalização

Threading e subprocess (para abrir janelas e executar Chrome em tela cheia) para automatização de na hora de transmitir a tela para televisão

⚠️ Observação: Este projeto não é complexo nem escalável, sendo feito sob medida para um cenário com limitações técnicas e operacionais. Ele atende a uma demanda prática imediata e é resultado de esforço adaptativo frente a restrições de TI e tempo disponível.
