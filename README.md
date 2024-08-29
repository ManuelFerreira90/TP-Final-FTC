<h1>TP-Final-FTC</h1>

<p><strong>Trabalho Prático Final da Disciplina de Fundamentos da Teoria da Computação</strong></p>

<p>Este repositório contém o trabalho prático final da disciplina de <strong>Fundamentos da Teoria da Computação</strong>.</p>

<h2>Instalação</h2>

<p>Antes de executar o projeto, é necessário instalar as bibliotecas externas listadas no arquivo <code>requirements.txt</code>. Para fazer isso, utilize o seguinte comando:</p>

<pre><code>!pip install -r requirements.txt</code></pre>

<p>Após a instalação completa das bibliotecas, você poderá executar o trabalho final rodando o arquivo <code>teste.py</code>.</p>

<h2>Execução</h2>

<p>Ao executar o arquivo, será aberta uma tela GUI, onde você poderá carregar um autômato por meio do botão <strong>"Carregar Autômato"</strong>.</p>

<p>Ao clicar nesse botão, uma janela será apresentada para selecionar um documento <code>.txt</code> contendo as informações sobre o autômato.</p>

<p>Após selecionar o arquivo, o autômato será carregado na memória, permitindo adicionar ingredientes na caixa de texto, adicionando o ingrediente por meio do botão "Adicionar Ingrediente".</p>


A cada ingrediente adicionado, uma imagem representativa do ingrediente será vista na tela. Caso seja atingido algum estado de errado por meio de uma mistura errada de ingredientes, é automaticamente informado para o usuário. Caso seja atingido algum estado final, ou seja, a mistura dos ingredientes resultou em uma das poções finais, é automaticamente informado para o usuário.