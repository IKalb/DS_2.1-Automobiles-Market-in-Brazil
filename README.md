# DS_2.1 Automobiles Market in Brazil
 Generate graphics of any model and period, since 2003, sold in Brazil

 Projeto de Análise de Dados DS_2.1

HISTÓRICO
O Projeto Carros foi iniciado para aplicar e desenvolver o conhecimento em linguagem Python e em análise de Dados. Seu objetivo era responder qual o impacto de  determinada campanha publicitária nas vendas do modelo VW Polo.
Na primeira fase, cada problema foi tratado em um módulo separado até alcançar uma solução satisfatória:
 1.- Baixar os arquivos em pdf do site.
 2.- Ler as duas tabelas escolhidas e gerar os Dataframes.
 3.- Limpar os dados.
 4.- Mesclar todos os dataframes em um único master.
 5.- Preparar o dataframe para gerar os gráficos.
 6.- Gerar os gráficos.

Nesta fase foram baixados e lidos 68 arquivos em pdf cobrindo o período de janeiro de 2017 a agosto de 2022. Foram programados 10 gráficos para analisar os dados.
Por fim escrevi um relatório apresentando o resultado da análise.
Nos meses seguintes os dados e gráficos foram atualizados com os novos relatórios disponibilizados, e melhorias foram sendo acrescentadas ao código.

No projeto DS_1.3 foi implementada a programação funcional, e todo o código em um único módulo.

Com o projeto estabilizado chegou o momento de torna-lo mais útil. O site de onde obtive os dados tem relatórios desde janeiro de 2003, o Projeto DS_2.0 foi baixar todos os arquivos e gerar o master com todos os automóveis comercializados desde então. O maior desafio foi corrigir a leitura dos arquivos devido às diversas mudanças na formatação do relatório.
O Projeto DS_2.1 usa os dados históricos levantados.

OBJETIVO  do DS_2.1
Permitir ao usuário encontrar as quantidades de cada modelo de automóvel vendido no Brasil a partir de 2003. Gerar os gráficos de desempenho de qualquer fabricante/modelo e no período escolhido pelo usuário.

DESCRIÇÃO
São dois módulos:
No módulo “Update_master” é verificado a necessidade de atualizar, se o usuário pedir, o dataframe master é atualizado e salvo.

O módulo “Show_results”, mostra uma lista de todas as marcas da lista para o usuário escolher uma, depois mostra todos os modelos desta marca para escolha. Ne sequencia pergunta o período a analisar, por fim gera os gráficos e os salva na pasta indicada.

COMO USAR
Copie ambos os códigos para sua máquina, atualize os path conforme necessário e salve o “master dataframe” na path apropriado.
Rode primeiro o módulo “update_master”, até você ter o master do mês corrente.
Depois rode o “show_results”, e veja os gráficos de desempenho do modelo escolhido.

COLABORAÇÃO
Sugestões e melhorias são bem-vindas.

Autor – ivo.kalb@gmail.com

