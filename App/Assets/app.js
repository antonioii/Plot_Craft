/* ===== I18N quick guide ===============================================
   - All textual content lives in the I18N object (per language).
   - Each page/topic has { title, body }.
   - Small UI strings live in I18N[lang].ui (e.g., menu toggles).
   - setLang(lang) switches the language and re-renders the page.
   - refreshMenuLabels(lang) updates all menu labels and UI microcopy
     so the sidebar reflects the active language.
======================================================================= */

/* ===== Store the current language ===== */
const LANG_KEY = 'manual_lang';
const DEFAULT_LANG = localStorage.getItem(LANG_KEY) || 'pt';

/* ===== Language dictionary with the content ===== */
const I18N = {
  //================================= PORTUGUESE =======================================================================
  pt: {
    introduction: {
      title: 'Introdução',
      body: `
        <p class="lead">Bem-vindo ao <strong>PlotCraft</strong>!</p>
        <p>O PlotCraft é uma Prova de Conceito (do inglês, <em>Proof of Concept</em> – PoC) criada a fim de mostrar como
        os modelos de linguagem de grande escala (LLMs) atuais são capazes de auxiliar na escrita de textos longos de
        ficção, assim criando livros inteiros consistentes internamente.</p>
        <br>
        <p>Este manual apresenta as principais funcionalidades do programa e está dividido em seções:</p>
        <ul>
          <li><strong>Introdução</strong>: Esta página que visa introduzir o usuário no contexto do projeto</li>
          <li><strong>Chaves de API</strong>: Seção que explica o que são, como adquirir e configurar chaves de API</li>
          <li><strong>Comece rápido aqui</strong>: Um tutorial passo-a-passo para a criação rápida com a ferramenta</li>
          <li><strong>Detalhes de cada tela</strong>: Uma explicação detalhada de cada tela dentro do programa</li>
          <li><strong>Mais sobre LLMs</strong>: Uma explicação mais profunda sobre como o programa funciona por trás dos
          panos, ideal para desenvolvedores criarem suas próprias soluções ou alterarem este projeto inicial</li>
        </ul>
        <br>
        <p>Este projeto é uma iniciativa de Antonio Sérgio C.C.II como projeto de conclusão de curso para o bacharelado
        em Ciência da Computação pela Faculdade Paulista – UNIP.</p>
        <p>
          <a href="https://www.linkedin.com/in/antonio-s%C3%A9rgio-costa-carpinteiro-ii-929179170/" target="_blank" 
          rel="noopener">LINKEDIN</a>
          |
          <a href="https://github.com/antonioii/PlotCraft" target="_blank" rel="noopener">GITHUB</a>
        </p>
      `
    },

    'api-keys': {
      title: 'Chaves de API',
      body: `
        <h2>O que são Chaves de API?</h2>
        <p>Logo na tela inicial do programa, será pedido para que você escolha um modelo de inteligência artificial
        (Large Language Model - LLM) e sua chave de API para acessar ele. Mas o que é esse chave de API e como
        conseguir uma?</p>
        <p>Basicamente, o PlotCraft se conecta a um serviço externo (como o GPT da OpenAI) que oferece acesso a
        uma inteligência artificial. Para fazer essa conexão, é usada uma “chave de API” que, basicamente, funciona
        como uma senha que permite acessar tal serviço externo. Dito de outra forma, uma Chave de API (do inglês,
        Application Programming Interface) é um código alfanumérico único que funciona como uma senha. Ela permite
        que programas, como o PlotCraft, se conectem e acessem serviços externos — por exemplo, modelos de linguagem
        (LLMs) ou outras ferramentas na nuvem. Sem essa chave, o acesso aos recursos oferecidos pelo serviço não é
        possível.</p>
        <p>Cada fornecedor de LLMs tem sua própria forma de gerar e utilizar chaves de API, além de políticas de
        cobrança. É fundamental, antes de gerar sua chave, verificar o preço praticado pelo serviço e entender o método
        de pagamento disponível.</p>
        <p>No caso do PlotCraft, utilizamos a chave de API da OpenAI para acessar o modelo “GPT-4o-mini”. O serviço
        da OpenAI trabalha com pagamento pré-pago, calculado conforme o uso de tokens (unidades de texto) e requisições.
        Assim, inicialmente o usuário deposita um valor no site da OpenAI que é debitado conforme o programa vai sendo
        usado. É importante destacar que não existe risco de débito negativo ou geração de dívida — o uso é limitado
        ao saldo disponível, desde que você não configure recargas automáticas. Também vale ressaltar que o uso da
        maioria dos modelos é de baixíssimo custo. Por exemplo, carregamos um crédito inicial de R$40,00 BRL
        (aproximadamente $8.00 USD). Após vários testes do programa com a geração de diversos livros (cada um com
        aproximadamente 50-60 mil palavras), o consumo total foi de apenas $0.44 USD, ou R$2,35 — um valor irrisório
        para o volume de texto gerado.</p>
        <p>Para consultar os preços atuais de uso do modelo “GPT-4o-mini”, acesse o painel de preços da OpenAI aqui
        <a href="https://platform.openai.com/docs/pricing" target="_blank">OpenAI Pricing</a></p>
        <br>
        <h3>Como conseguir uma Chave de API? (Exemplo da OpenAI)</h3>
        <p>Veja este vídeo aqui <a href="https://www.youtube.com/watch?v=Y9gOf4we3tk" target="_blank">YouTube</a> ou
        siga o passo-a-passo abaixo:</p>
        <ol>
          <li>Acesse a plataforma OpenAI (<a href="https://platform.openai.com" target="_blank">platform.openai.com
          </a>)</li>
          <li>Clique em “Sign Up” para criar uma conta ou em “Login” se já possuir uma.</li>
          <li>Após o login, você terá acesso à área de projetos. Clique em “Create Project” no canto superior esquerdo
          da tela, dê um nome, e confirme.</li>
          <li>Verifique seu número de telefone</li>
          <li>Antes de criar a chave, será solicitado que você verifique seu celular. Insira o número, receba o SMS com
          o código e informe-o na tela.</li>
          <li>Acesse o menu lateral da plataforma e selecione “API Keys”.</li>
          <li>Clique em “Create new secret key”.</li>
          <li>Escolha um nome para a chave, selecione o projeto desejado e defina as permissões (é possível restringir
          quais modelos e recursos a chave terá acesso).</li>
          <li>Clique em “Create” para gerar a chave.</li>
          <li>⚠️ <u><strong>Atenção</strong></u>: Copie imediatamente a chave exibida e salve-a em um local onde você
          poderá acessar depois (por exemplo, um arquivo de texto em seu computador), pois ela será mostrada apenas
          uma vez.</li>
          <li>Você irá precisar então adicionar saldo</li>
          <li>No menu, acesse “Usage” para verificar seu crédito atual.</li>
          <li>Para comprar créditos, clique em “Buy credits”, preencha os dados de pagamento, escolha o valor
          (mínimo $5 USD) e confirme a transação.</li>
          <li>⚠️ <u><strong>Atenção</strong></u>: Você pode optar por recarga automática, mas ela é opcional,
          deixe desmarcado pois assim garante que o modelo jamais use mais do que o inicialmente colocado</li>
        </ol>
        <br>
        <p>⚠️ <u><strong>Atenção</strong></u>: Cada chave é única, pessoal e vinculada à sua conta. Caso compartilhe
        com terceiros, estes podem consumir seus créditos.</p>
        <br>
        <h3>Como guardar uma Chave de API de forma segura para re-utilização?</h3>
        <ul>
          <li>Nunca compartilhe sua chave em redes sociais, prints ou repositórios públicos.</li>
          <li>Salve em um arquivo local protegido de terceiros, ou apenas delete após o uso e crie outra quando for
          usar novamente o programa.</li>
          <li>Se usar GitHub ou outros serviços de versionamento, adicione esse arquivo ao .gitignore para que não
          seja enviado ao repositório.</li>
          <li>Caso suspeite que sua chave foi exposta, revogue-a imediatamente e gere uma nova no site do provedor
          (criar chaves é um processo gratuito).</li>
        </ul>
      `
    },

    'fast-start': {
        title: 'Comece rápido aqui',
        body: `
          <p>Primeiramente, você irá precisar de uma Chave de API e créditos na plataforma da OpenAI (por enquanto,
          o único provedor de IA configurado no projeto). Caso não tenha, veja a seção “Chaves de API” para mais
          informações sobre como adquirir e criar uma.</p>

          <h3>Passo-a-passo:</h3>

          <h4>1. Início</h4>
          <p>Na tela inicial, clique em “New Project” e insira seus dados da API. Escolha o modelo “GPT-4o-nano”,
          atualmente o único disponível no projeto. Caso já tenha algum projeto salvo, apenas clique em “Load Project”
          e selecione-o para continuar de onde parou.</p>
          <img src="./manual-screens/initial.png" alt="Tela inicial">
          <p><em>Obs:</em> Toda vez que avançamos de tela, o projeto é salvo automaticamente. Em algumas telas
          (capítulos e beats), quando editamos o texto, também é salvo automaticamente.</p>
          <br>
          <h4>2. Títulos e Resumos</h4>
          <p>Na tela de títulos e resumos, preencha com o título do seu livro e um breve resumo (sinopse), então
          clique em “Outline my plot” para seguir para o próximo passo.</p>
          <img src="./manual-screens/titles1.png" alt="Títulos 1">
          <p>Caso não tenha uma ideia consolidada, você pode marcar a caixa de seleção (“Mark this checkbox...”) e
          clicar em “Outline my plot” para abrir uma janela de geração de ideias, na qual poderá inserir elementos,
          gerar resumos e escolher entre eles.</p>
          <img src="./manual-screens/titles2.png" alt="Títulos 2">
          <br>
          <h4>3. Quadro de Referências</h4>
          <p>Nesta etapa, será gerado um quadro de referências com os elementos narrativos (“Lugares e Objetos”;
          “Personagens Principais”; “Acontecimentos Principais”). Leia os elementos gerados, edite-os e crie novos.
          O processo criativo é fundamental para termos uma história coerente e de boa qualidade.</p>
          <img src="./manual-screens/ref-board.png" alt="Quadro de referência">
          <br>
          <h4>4. Atos Narrativos</h4>
          <p>Nesta tela, são gerados os três atos principais da obra em criação. Mais uma vez, é fundamental que
          você leia os elementos gerados e os edite para criar uma narrativa coerente e coesa, antes de aceitá-los
          para prosseguir.</p>
          <img src="./manual-screens/acts.png" alt="Atos">
          <br>
          <h4>5. Capítulos</h4>
          <p>Na tela de capítulos, há uma caixa de seleção com os capítulos gerados. Ao selecionar um capítulo, o
          resumo correspondente aparece abaixo para que você possa editá-lo. Sempre que trocamos de capítulo, o
          resumo é automaticamente salvo. Sinta-se à vontade para criar novos capítulos e excluir outros.</p>
          <img src="./manual-screens/chapters.png" alt="Capítulos">
          <p>(Tela com os capítulos)</p>
          <br>
          <img src="./manual-screens/chapters2.png" alt="Capítulos - criação">
          <p>(Tela de criação de novos capítulos)</p>
          <br>
          <br>
          <h4>6. Beats</h4>
          <p>Após aceitar os capítulos da tela anterior, são gerados os “Story-Beats”. Eles representam trechos
          com acontecimentos importantes dentro de cada capítulo, podendo ser entendidos como resumos de subcapítulos
          que fazem o capítulo central se desenvolver. Assim como na tela anterior, você pode selecionar os capítulos
          e cada “beat” dentro deles para exibir os trechos a serem editados. Edite, exclua e crie novos conforme
          seu processo criativo.</p>
          <img src="./manual-screens/beats1.png" alt="Beats">
          <p>(Tela com os beats)</p>
          <br>
          <img src="./manual-screens/beats2.png" alt="Edição de Beats">
          <p>(Tela de criação de novos beats)</p>
          <br>
          <br>
          <h4>7. Geração Final</h4>
          <p>Após aceitar os beats da tela anterior, o programa iniciará a geração do rascunho final. Esse rascunho
          contém demarcações claras de capítulos, acompanhados de um breve resumo (marcados pelo termo “CAPITULUM LIBRI”),
          a fim de auxiliar na edição final da obra.</p>
          <img src="./manual-screens/final.png" alt="Tela final">
          <br>
          <p>Por fim, copie para a área de transferência, ou salve para refinamento posterior no seu editor de texto
          favorito!</p>
          <br>
          <br>
          <p><strong>Pronto! Simples assim!</strong></p>
        `
      },

    'window-initial': {
      title: 'Janela Inicial',
      body: `
        <p>Apresentação e criação do projeto.</p>

        <p>Na tela inicial, há um botão para criar novos projetos (“New Project”), um botão para carregar projetos
        não terminados (“Load Project”) e um botão de Instruções.</p>

        <p>Tanto o “New Project” quanto o “Load Project” abrirão um pop-up solicitando que você selecione um modelo
        e insira a sua chave de API. O “New Project” iniciará a etapa de geração de <em>títulos</em> e resumos; o
        “Load Project” retomará do ponto em que o projeto anterior foi interrompido. Para carregar um projeto
        previamente salvo, selecione o arquivo <code>.json</code> correspondente.</p>

        <p>O processo de seleção do modelo de linguagem e da chave de API pode ser modificado ao longo das telas
        seguintes de desenvolvimento do projeto.</p>

        <p>Atualmente, o único modelo disponível é o “GPT-4o-nano”.</p>

        <img src="./manual-screens/initial.png" alt="Tela inicial">

        <p><em>Obs:</em> Toda vez que avançamos de tela, o projeto é salvo automaticamente. Em algumas telas
        (capítulos e beats), quando editamos o texto, ele também é salvo automaticamente.</p>
        <br>
  `
    },

    'window-title-resume': {
      title: 'Título & Sinopse',
      body: `
        <p>Definir o título e a sinopse do livro.</p>

        <p>Na tela de títulos e resumos, preencha com o título do seu livro e um breve resumo (sinopse),
        então clique em “Outline my plot” para seguir para o próximo passo.</p>
        <img src="./manual-screens/titles1.png" alt="Títulos 1">
        <br><br>

        <p>Caso não tenha uma ideia consolidada, você pode marcar a caixa de seleção (“Mark this checkbox...”)
        e clicar em “Outline my plot” para abrir uma janela de geração de ideias, na qual poderá inserir elementos,
        gerar resumos e escolher entre eles.</p>
        <img src="./manual-screens/titles2.png" alt="Títulos 2">

        <p>Nessa tela de sugestões para títulos e resumos, você pode preencher informações-chave:</p>
        <ul>
          <li><i>Gênero literário</i> (ex: ficção, fantasia, etc.)</li>
          <li><i>Mercado editorial</i> (ex: autoajuda, leitura de praia, jovens adultos, etc.)</li>
          <li><i>Gênero secundário</i> (ex: romance, suspense, ficção histórica, etc.)</li>
          <li><i>Formato</i> (ex: e-book, livro longo de capa dura, etc.)</li>
          <li><i>Tom/Estilo narrativo</i> (ex: inspiracional, sombrio, comédia, etc.)</li>
        </ul>

        <p>Após preencher e clicar no botão de sugestões, uma lista com cerca de 20 opções será exibida para que
        você escolha uma. Uma vez escolhida, ao clicar no botão para selecionar a sinopse, o programa fechará o pop-up
        e preencherá automaticamente as informações na tela original de títulos e resumos. O usuário poderá então editar,
        acrescentando ou removendo elementos conforme seu próprio processo criativo.</p>
      `
    },

    'window-reference-board': {
      title: 'Quadro de Referências',
      body: `
        <p>Organizar os elementos narrativos principais.</p>

        <p>Nesta etapa, será gerado um quadro de referências com os elementos narrativos:
          <em>“Lugares e Objetos”</em>, <em>“Personagens Principais”</em> e <em>“Acontecimentos Principais”</em>.
          Leia os elementos gerados, edite-os e crie novos conforme necessário. Esse refinamento é essencial
          para manter coerência e qualidade ao longo da história.</p>

        <img src="./manual-screens/ref-board.png" alt="Quadro de referência">
        <br><br>

        <p>Dicas rápidas:</p>
        <ul>
          <li>Padronize nomes de personagens e locais (evita inconsistências mais à frente).</li>
          <li>Conecte acontecimentos principais aos objetivos dos personagens.</li>
          <li>Adicione objetos/lugares relevantes que retornem em capítulos futuros.</li>
        </ul>

        <p>Quando estiver satisfeito, avance para a etapa de <strong>Atos</strong>.</p>
      `
    },

    'window-acts': {
      title: 'Atos Narrativos',
      body: `
        <p>Estruturar a obra em três atos principais.</p>

        <p>Nesta tela, o programa gera automaticamente os três atos narrativos fundamentais da história.
        É altamente recomendável que você leia com atenção os elementos gerados, edite-os e faça os ajustes necessários.
        Essa etapa é essencial para garantir que a narrativa se mantenha coerente, coesa e bem estruturada.</p>

        <img src="./manual-screens/acts.png" alt="Atos narrativos">

        <p><strong>Dicas rápidas:</strong></p>
        <ul>
          <li>No Ato I, estabeleça personagens, cenários e conflitos iniciais.</li>
          <li>No Ato II, desenvolva os conflitos, explore reviravoltas e faça a narrativa crescer em complexidade.</li>
          <li>No Ato III, apresente a resolução, amarre os principais elementos e conclua a trajetória dos personagens.</li>
        </ul>

        <p>Após revisar e aceitar os atos, você poderá avançar para a etapa de <strong>Capítulos</strong>.</p>
      `
    },

    'window-chapters': {
      title: 'Capítulos',
      body: `
        <p>Definir e revisar os capítulos da obra.</p>

        <p>Na tela de capítulos, há uma lista com os capítulos gerados. Ao selecionar um capítulo,
        o respectivo <em>resumo</em> aparece abaixo para edição. Sempre que você troca de capítulo,
        o resumo é salvo automaticamente. Sinta-se à vontade para <strong>criar novos capítulos</strong>
        e <strong>excluir</strong> aqueles que não desejar manter.</p>

        <img src="./manual-screens/chapters.png" alt="Capítulos">
        <br>

        <img src="./manual-screens/chapters2.png" alt="Criação de capítulos">
        <br>

        <p><strong>Dicas rápidas:</strong></p>
        <ul>
          <li>Verifique a consistência entre o resumo do capítulo e os <em>atos</em> definidos anteriormente.</li>
          <li>Mantenha um objetivo claro para cada capítulo (gancho inicial, desenvolvimento e fechamento).</li>
          <li>Prefira títulos curtos e informativos; eles facilitam a visualização do todo.</li>
        </ul>

        <p>Quando finalizar os capítulos, avance para a etapa de <strong>Beats</strong>.</p>
      `
    },

    'window-beats': {
      title: 'Beats',
      body: `
        <p>Estruturar cada capítulo em <em>story-beats</em> (trechos fundamentais).</p>

        <p>Após aceitar os capítulos na tela anterior, são gerados os “Story-Beats”.
        Eles representam acontecimentos importantes dentro de cada capítulo e podem ser entendidos
        como resumos de <em>subcapítulos</em> que fazem o enredo avançar.</p>

        <p>Assim como na tela de capítulos, você pode selecionar cada beat para exibir seu texto e editá-lo.
        Além disso, é possível <strong>criar novos beats</strong> e <strong>excluir</strong> os que não forem úteis,
        moldando o enredo conforme o seu processo criativo.</p>

        <img src="./manual-screens/beats1.png" alt="Beats">
        <br>

        <img src="./manual-screens/beats2.png" alt="Edição de beats">
        <br>

        <p><strong>Dicas rápidas:</strong></p>
        <ul>
          <li>Use os beats para detalhar conflitos, reviravoltas ou revelações importantes.</li>
          <li>Garanta que cada beat contribua para o desenvolvimento do capítulo.</li>
          <li>Mantenha a progressão natural: cada beat deve levar logicamente ao próximo.</li>
        </ul>

        <p>Quando estiver satisfeito, avance para a etapa de <strong>Geração Final</strong>.</p>
      `
    },

    'window-finishing': {
      title: 'Finalização',
      body: `
        <p>Gerar o rascunho final do seu livro.</p>

        <p>Após aceitar os beats da tela anterior, o programa inicia a etapa de <strong>Geração Final</strong>.
        Nessa fase, o sistema cria um rascunho completo, estruturado com divisões claras de capítulos
        e acompanhados por breves resumos (marcados pelo termo <em>“CAPITULUM LIBRI”</em>).
        Esse formato ajuda a organizar o material para revisão e edição posteriores.</p>

        <img src="./manual-screens/finishing.png" alt="Finalização">

        <p><strong>Dicas rápidas:</strong></p>
        <ul>
          <li>Revise o rascunho com atenção e anote pontos que precisam ser reescritos ou expandidos.</li>
          <li>Use os resumos de cada capítulo como guia para verificar consistência na narrativa.</li>
          <li>Faça backups do arquivo em diferentes locais para garantir segurança do material.</li>
        </ul>

        <p>Por fim, copie o rascunho para a área de transferência ou salve-o em seu editor de texto favorito
        para o refinamento final.</p>

        <br>
        <p><strong>Parabéns! Você concluiu todas as etapas do PlotCraft 🎉</strong></p>
      `
    },

    'llms-depth': {
      title: 'Mais sobre LLMs',
      body: `
        <p><strong>Dicas rápidas de prompts e limites.</strong></p>

        <p>Este projeto foi elaborado pensando em um fluxo de trabalho que torna possível utilizar 
        modelos de linguagem de grande escala (LLMs) para escrever livros longos e consistentes.
        O objetivo não é apenas mostrar a tecnologia, mas também inspirar novas aplicações criativas.</p>

        <p>Ao usar LLMs, lembre-se de:</p>
        <ul>
          <li>Ser específico nos <em>prompts</em>, fornecendo contexto, estilo e objetivo desejado.</li>
          <li>Dividir tarefas complexas em etapas menores (por exemplo, título → sinopse → capítulos → beats).</li>
          <li>Reconhecer os limites dos modelos: eles podem errar, ser repetitivos ou imprecisos — revise sempre.</li>
        </ul>

        <p><strong>Saiba mais sobre LLMs em fontes confiáveis:</strong></p>
        <ul>
          <li><a href="https://platform.openai.com/docs" target="_blank">Documentação da OpenAI</a></li>
          <li><a href="https://huggingface.co/learn/nlp-course" target="_blank">Curso de NLP da Hugging Face</a></li>
          <li><a href="https://www.deeplearning.ai/" target="_blank">DeepLearning.AI</a></li>
        </ul>

        <p><strong>Autor do projeto:</strong> Antonio Sérgio C.C. II  
        <br>
        <a href="https://www.linkedin.com/in/antonio-s%C3%A9rgio-costa-carpinteiro-ii-929179170/" target="_blank">LinkedIn</a> | 
        <a href="https://github.com/antonioii/PlotCraft" target="_blank">GitHub</a></p>
      `
    },


    ui: {
      menuEachWindow: 'Detalhes de cada tela',
      collapse: '(Recolher menu)'
    }

  //================================= ENGLISH =========================================================================
  },
  en: {
    introduction: {
      title: 'Introduction',
      body: `
        <p class="lead">Welcome to <strong>PlotCraft</strong>!</p>
        <p>PlotCraft is a Proof of Concept (PoC) designed to demonstrate how current large language models (LLMs)
        can help write long-form fiction, enabling entire books that remain internally consistent.</p>
        <br>
        <p>This manual presents the main features of the program and is organized into sections:</p>
        <ul>
          <li><strong>Introduction</strong>: This page introducing the project's context</li>
          <li><strong>API Keys</strong>: What API keys are, how to get them, and how to configure them</li>
          <li><strong>Fast Start</strong>: A step-by-step quickstart tutorial</li>
          <li><strong>Each window</strong>: A detailed explanation of every screen in the program</li>
          <li><strong>More about LLMs</strong>: A deeper look at how the program works under the hood—ideal for
          developers to extend or adapt this initial project</li>
        </ul>
        <br>
        <p>This project is an initiative by Antonio Sérgio C.C. II as a final project for the B.Sc. in Computer
        Science at "Faculdade Paulista" - UNIP.</p>
        <p>
          <a href="https://www.linkedin.com/in/antonio-s%C3%A9rgio-costa-carpinteiro-ii-929179170/" target="_blank"
          rel="noopener">LINKEDIN</a>
          |
          <a href="https://github.com/antonioii/PlotCraft" target="_blank" rel="noopener">GITHUB</a></p>
      `
    },

    'api-keys': {
      title: 'API Keys',
      body: `
        <h2>What are API Keys?</h2>
        <p>On the initial screen of the program, you will be asked to choose a Large Language Model (LLM) and provide
        its API key to access it. But what is an API key, and how can you get one?</p>
        <p>Basically, PlotCraft connects to an external service (such as OpenAI's GPT) that provides access to artificial
        intelligence. To establish this connection, it uses an “API key” that essentially works like a password. In
        other words, an API Key (from Application Programming Interface) is a unique alphanumeric code that functions
        as a password. It allows programs like PlotCraft to connect to and access external services — for example,
        language models (LLMs) or other cloud tools. Without this key, access to the resources offered by the service
        is not possible.</p>
        <p>Each LLM provider has its own way of generating and using API keys, as well as billing policies. Before
        generating your key, it is essential to check the pricing and the available payment method.</p>
        <p>In the case of PlotCraft, we use the OpenAI API key to access the “GPT-4o-mini” model. OpenAI works with
        a prepaid system, calculated according to the use of tokens (text units) and requests. Initially, the user
        deposits an amount on the OpenAI website, which is then deducted as the program is used. Importantly, there
        is no risk of overdraft or debt — usage is limited to the available balance, as long as you don't set up automatic
        cash refills. It is also worth noting that the cost of using most models is extremely low. For example, we
        loaded an initial credit of BRL 40.00 (approximately USD 8.00). After several program tests generating multiple
        books (each with around 50-60 thousand words), the total consumption was only USD 0.44, or BRL 2.35 — a
        negligible cost for the volume of text generated.</p>
        <p>To check the current prices of the “GPT-4o-mini” model, access the OpenAI pricing panel here <a
        href="https://platform.openai.com/docs/pricing" target="_blank">OpenAI Pricing</a></p>
        <br>
        <h3>How to get an API Key? (OpenAI Example)</h3>
        <p>Watch this video <a href="https://www.youtube.com/watch?v=Y9gOf4we3tk" target="_blank">YouTube</a> or
        follow the step-by-step instructions below:</p>
        <ol>
          <li>Go to the OpenAI platform (<a href="https://platform.openai.com" target="_blank">platform.openai.com</a>)</li>
          <li>Click “Sign Up” to create an account or “Login” if you already have one.</li>
          <li>After logging in, you will have access to the project area. Click “Create Project” in the top left
          corner of the screen, give it a name, and confirm.</li>
          <li>Verify your phone number</li>
          <li>Before creating the key, you will be asked to verify your cell phone. Enter the number, receive the
          SMS with the code, and enter it on the screen.</li>
          <li>Access the platform's side menu and select “API Keys”.</li>
          <li>Click “Create new secret key”.</li>
          <li>Choose a name for the key, select the desired project, and define the permissions (it is possible to
          restrict which models and resources the key will have access to).</li>
          <li>Click “Create” to generate the key.</li>
          <li>⚠️ <u><strong>Attention</strong></u>: Immediately copy the displayed key and save it somewhere
          you can access later (for example, a text file on your computer), as it will only be shown once.</li>
          <li>You will then need to add balance</li>
          <li>In the menu, go to “Usage” to check your current credit.</li>
          <li>To purchase credits, click “Buy credits”, fill in the payment details, choose the amount (minimum USD 5),
          and confirm the transaction.</li>
          <li>⚠️ <u><strong>Attention</strong></u>: You can opt for automatic recharge, but it is optional. Leave it
          unchecked to ensure the model never uses more than the initially deposited amount.</li>
        </ol>
        <br>
        <p>⚠️ <u><strong>Attention</strong></u>: Each key is unique, personal, and linked to your account. If you
        share it with third parties, they may consume your credits.</p>
        <br>
        <h3>How to store an API Key securely for reuse?</h3>
        <ul>
          <li>Never share your key on social networks, screenshots, or public repositories.</li>
          <li>Save it in a local file protected from third parties, or delete it after the use and re-create on
          another ocasion.</li>
          <li>If you use GitHub or other versioning services, add this file to .gitignore so it is not uploaded to
          the repository.</li>
          <li>If you suspect your key has been exposed, revoke it immediately and generate a new one on the provider's
          website (creating keys is a free process).</li>
        </ul>
      `
    },

    'fast-start': {
        title: 'Quick Start',
        body: `
          <p>First, you will need an API Key and credits on the OpenAI platform (for now, the only AI provider
          configured in this project). If you don't have one yet, see the “API Keys” section for more information
          on how to acquire and create one.</p>

          <h3>Step-by-step:</h3>

          <h4>1. Start</h4>
          <p>On the initial screen, click “New Project” and enter your API data. Choose the model “GPT-4o-nano”,
          currently the only one available in the project. If you already have a saved project, simply click “Load
          Project” and select it to continue where you left off.</p>
          <img src="./manual-screens/initial.png" alt="Initial screen">
          <p><em>Note:</em> Every time you move forward to the next screen, the project is automatically saved.
          On some screens (chapters and beats), when you edit the text, it is also saved automatically.</p>
          <br>
          <h4>2. Titles and Summaries</h4>
          <p>On the titles and summaries screen, fill in the title of your book and a short summary (synopsis),
          then click “Outline my plot” to proceed to the next step.</p>
          <img src="./manual-screens/titles1.png" alt="Titles 1">
          <p>If you don't yet have a consolidated idea, you can check the box (“Mark this checkbox...”) and click
          “Outline my plot” to open an idea generation window where you can enter elements, generate summaries,
          and select them.</p>
          <img src="./manual-screens/titles2.png" alt="Titles 2">
          <br>
          <h4>3. Reference Board</h4>
          <p>At this stage, a reference board is generated with narrative elements (“Places and Objects”; “Main
          Characters”; “Main Events”). Read the generated elements, edit them, and create new ones. The creative
          process is essential for building a coherent and high-quality story.</p>
          <img src="./manual-screens/ref-board.png" alt="Reference board">
          <br>
          <h4>4. Narrative Acts</h4>
          <p>On this screen, the three main acts of the work are generated. Once again, it is essential that you
          read the generated elements and edit them to create a coherent and cohesive narrative before accepting
          them to move forward.</p>
          <img src="./manual-screens/acts.png" alt="Acts">
          <br>
          <h4>5. Chapters</h4>
          <p>On the chapters screen, there is a selection box with the generated chapters. By selecting a chapter,
          its summary will be displayed below for editing. Each time you switch chapters, the summary is automatically
          saved. Feel free to create new chapters and delete others.</p>
          <img src="./manual-screens/chapters.png" alt="Chapters">
          <p>(Chapters screen)</p>
          <br>
          <img src="./manual-screens/chapters2.png" alt="Chapters - creation">
          <p>(New chapters creation screen)</p>
          <br>
          <br>
          <h4>6. Beats</h4>
          <p>After accepting the chapters from the previous screen, “Story-Beats” are generated. These are sections
          with important events within each chapter and can be understood as subchapter summaries that develop the
          central chapter. As in the previous screen, here you can select the chapters and each “beat” within them
          to display the sections to be edited. You should edit, delete, and create new ones as part of your creative
          process.</p>
          <img src="./manual-screens/beats1.png" alt="Beats">
          <p>(Beats screen)</p>
          <br>
          <img src="./manual-screens/beats2.png" alt="Beats editing">
          <p>(New beats creation screen)</p>
          <br>
          <br>
          <h4>7. Final Generation</h4>
          <p>After accepting the beats from the previous screen, the program will begin generating the final draft.
          The draft contains clear chapter markings along with a short summary (marked by the term “CAPITULUM LIBRI”)
          to assist in the final editing of the work.</p>
          <img src="./manual-screens/final.png" alt="Final screen">
          <br>
          <p>Finally, copy it to the clipboard, or save it for further refinement in your favorite text editor!</p>
          <br>
          <br>
          <p><strong>That's it! Simple as that!</strong></p>
        `
      },

    'window-initial': {
      title: 'Initial Window',
      body: `
        <p>Presentation and project creation.</p>

        <p>On the initial screen, there is a button to create new projects (“New Project”), a button to load
        unfinished projects (“Load Project”), and an Instructions button.</p>

        <p>Both “New Project” and “Load Project” will open a pop-up asking you to select a model and enter your
        API key. “New Project” starts the generation step for <em>titles</em> and summaries; “Load Project” resumes
        from where the previous project stopped. To load a previously saved project, select its corresponding 
        <code>.json</code> file.</p>

        <p>The chosen language model and API key can be changed throughout the subsequent screens in the project's
        development.</p>

        <p>Currently, the only available model is “GPT-4o-nano”.</p>

        <img src="./manual-screens/initial.png" alt="Initial screen">

        <p><em>Note:</em> Every time you move to the next screen, the project is saved automatically. On some
        screens (chapters and beats), when you edit the text, it is also saved automatically.</p>
        <br>
      `
    },

    'window-title-resume': {
      title: 'Title & Synopsis',
      body: `
        <p>Define the book’s title and synopsis.</p>

        <p>On the titles and summaries screen, fill in the title of your book and a short summary (synopsis),
        then click “Outline my plot” to proceed to the next step.</p>
        <img src="./manual-screens/titles1.png" alt="Titles 1">
        <br><br>

        <p>If you don’t have a consolidated idea yet, you can check the box (“Mark this checkbox...”) and click
        “Outline my plot” to open an idea generation window where you can enter elements, generate summaries,
        and select among them.</p>
        <img src="./manual-screens/titles2.png" alt="Titles 2">

        <p>In this suggestions screen for titles and summaries, you can provide key information such as:</p>
        <ul>
          <li><i>Literary genre</i> (e.g., fiction, fantasy, etc.)</li>
          <li><i>Target market</i> (e.g., self-help, beach reads, young adults, etc.)</li>
          <li><i>Secondary genre</i> (e.g., romance, suspense, historical fiction, etc.)</li>
          <li><i>Format</i> (e.g., e-book, long hardcover book, etc.)</li>
          <li><i>Tone/Narrative style</i> (e.g., inspirational, dark, comedy, etc.)</li>
        </ul>

        <p>After filling in the fields and clicking the suggestion button, a list of about 20 options will
        appear for you to choose from. Once you select one and click the button to confirm the synopsis, the
        program will close the pop-up and automatically fill in the generated information on the original titles
        and summaries screen. You can then edit it, adding or removing elements as part of your own creative process.</p>
      `
    },

    'window-reference-board': {
      title: 'Reference Board',
      body: `
        <p>Organize the main narrative elements.</p>

        <p>At this stage, a reference board is generated with the narrative elements:
          <em>“Places & Objects”</em>, <em>“Main Characters”</em>, and <em>“Main Events”</em>.
          Read the generated entries, edit them, and create new ones as needed. This refinement is crucial
          to keep coherence and quality throughout the story.</p>

        <img src="./manual-screens/ref-board.png" alt="Reference board">
        <br><br>

        <p>Quick tips:</p>
        <ul>
          <li>Standardize names of characters and locations (prevents later inconsistencies).</li>
          <li>Connect main events to the characters’ goals.</li>
          <li>Add relevant objects/places that will reappear in future chapters.</li>
        </ul>

        <p>When you’re ready, proceed to the <strong>Acts</strong> stage.</p>
      `
    },

    'window-acts': {
      title: 'Narrative Acts',
      body: `
        <p>Structure the work into three main acts.</p>

        <p>On this screen, the program automatically generates the three fundamental narrative acts of the story.
        It is strongly recommended that you carefully read the generated elements, edit them, and make the
        necessary adjustments.
        This step is crucial to ensure the narrative remains coherent, cohesive, and well-structured.</p>

        <img src="./manual-screens/acts.png" alt="Narrative acts">

        <p><strong>Quick tips:</strong></p>
        <ul>
          <li>In Act I, establish the characters, setting, and initial conflicts.</li>
          <li>In Act II, develop the conflicts, explore twists, and increase the complexity of the narrative.</li>
          <li>In Act III, bring resolution, tie together the main elements, and conclude the characters' journeys.</li>
        </ul>

        <p>After reviewing and accepting the acts, you can move forward to the <strong>Chapters</strong> stage.</p>
      `
    },

    'window-chapters': {
      title: 'Chapters',
      body: `
        <p>Define and revise the book's chapters.</p>

        <p>On the chapters screen, you will see a list of generated chapters. When you select a chapter,
        its <em>summary</em> appears below for editing. Each time you switch chapters, the summary is
        saved automatically. Feel free to <strong>create new chapters</strong> and
        <strong>delete</strong> those you don't want to keep.</p>

        <img src="./manual-screens/chapters.png" alt="Chapters">
        <br>

        <img src="./manual-screens/chapters2.png" alt="Chapter creation">
        <br>

        <p><strong>Quick tips:</strong></p>
        <ul>
          <li>Check consistency between each chapter summary and the previously defined <em>acts</em>.</li>
          <li>Keep a clear goal for every chapter (hook, development, and closing).</li>
          <li>Prefer short, informative titles; they make the overall structure easier to see.</li>
        </ul>

        <p>When you finish the chapters, proceed to the <strong>Beats</strong> stage.</p>
      `
    },

    'window-beats': {
      title: 'Beats',
      body: `
        <p>Break down each chapter into fundamental <em>story-beats</em>.</p>

        <p>After accepting the chapters from the previous screen, “Story-Beats” are generated.
        They represent key events within each chapter and can be understood as
        <em>subchapter summaries</em> that move the plot forward.</p>

        <p>As with the chapters screen, you can select each beat to display its text and edit it.
        You can also <strong>create new beats</strong> and <strong>delete</strong> the ones you don't need,
        shaping the narrative according to your creative process.</p>

        <img src="./manual-screens/beats1.png" alt="Beats">
        <br>

        <img src="./manual-screens/beats2.png" alt="Beats editing">
        <br>

        <p><strong>Quick tips:</strong></p>
        <ul>
          <li>Use beats to highlight conflicts, twists, or important revelations.</li>
          <li>Ensure each beat contributes to the chapter's development.</li>
          <li>Maintain natural progression: each beat should logically lead to the next.</li>
        </ul>

        <p>When ready, proceed to the <strong>Final Generation</strong> stage.</p>
      `
    },

    'window-finishing': {
      title: 'Finishing',
      body: `
        <p>Generate the final draft of your book.</p>

        <p>After accepting the beats from the previous screen, the program starts the <strong>Final Generation</strong> stage.
        At this point, the system produces a complete draft, structured with clear chapter divisions
        and accompanied by short summaries (marked by the term <em>“CAPITULUM LIBRI”</em>).
        This format helps organize the material for later review and editing.</p>

        <img src="./manual-screens/finishing.png" alt="Finishing">

        <p><strong>Quick tips:</strong></p>
        <ul>
          <li>Carefully review the draft and note points that need rewriting or expansion.</li>
          <li>Use the chapter summaries as a guide to check consistency in the narrative.</li>
          <li>Back up the file in different locations to keep your material safe.</li>
        </ul>

        <p>Finally, copy the draft to the clipboard or save it into your favorite text editor
        for final refinement.</p>

        <br>
        <p><strong>Congratulations! You have completed all stages of PlotCraft 🎉</strong></p>
      `
    },

    'llms-depth': {
      title: 'More about LLMs',
      body: `
        <p><strong>Quick tips on prompts and limits.</strong></p>

        <p>This project was designed with a workflow that makes it possible to use 
        large language models (LLMs) to write long and consistent books.
        The goal is not only to demonstrate the technology but also to inspire new creative applications.</p>

        <p>When working with LLMs, keep in mind:</p>
        <ul>
          <li>Be specific in your <em>prompts</em>, providing context, style, and the desired outcome.</li>
          <li>Break down complex tasks into smaller steps (e.g., title → synopsis → chapters → beats).</li>
          <li>Acknowledge the limits of the models: they may make mistakes, repeat themselves, or be imprecise
          — always review.</li>
        </ul>

        <p><strong>Learn more about LLMs from credible sources:</strong></p>
        <ul>
          <li><a href="https://platform.openai.com/docs" target="_blank">OpenAI Documentation</a></li>
          <li><a href="https://huggingface.co/learn/nlp-course" target="_blank">Hugging Face NLP Course</a></li>
          <li><a href="https://www.deeplearning.ai/" target="_blank">DeepLearning.AI</a></li>
        </ul>

        <p><strong>Project Author:</strong> Antonio Sérgio C.C. II  
        <br>
        <a href="https://www.linkedin.com/in/antonio-s%C3%A9rgio-costa-carpinteiro-ii-929179170/" target="_blank">LinkedIn</a> | 
        <a href="https://github.com/antonioii/PlotCraft" target="_blank">GitHub</a></p>
      `
    },


    ui: {
      menuEachWindow: 'Each window details',
      collapse: '(Collapse menu)'
    }
  }
};

/* ===== Interface ===== */
const content = document.getElementById('content');
const collapseBtn = document.getElementById('collapseBtn');
const reopenBtn = document.getElementById('reopenBtn');
const btnPT = document.getElementById('btn-pt');
const btnEN = document.getElementById('btn-en');

/* ===== Simple State ===== */
const state = {
  lang: DEFAULT_LANG,
  topic: 'introduction'
};

/* ===== Hash routing (ex.: index.html#window-chapters) ===== */
function readHash(){
  const h = (location.hash || '').replace('#','').trim();
  if (h && I18N[state.lang][h]) state.topic = h;
}
window.addEventListener('hashchange', () => {
  readHash();
  renderPage(state.topic);
});

/* ===== Rendering ===== */
function renderPage(topic){
  const item = I18N[state.lang][topic];
  if(!item) return;
  content.innerHTML = `
    <h2 class="page-title">${item.title}</h2>
    <hr />
    <div class="page-body">${item.body}</div>
  `;
  markActive(topic);
  // Content focus after change the page
  content.focus();
}

function markActive(topic){
  document.querySelectorAll('.nav-link, .nav-sublink').forEach(el => el.classList.remove('active'));
  document.querySelectorAll(`[data-topic="${topic}"]`).forEach(el => el.classList.add('active'));
}

/* ===== Sidebar Action ===== */
document.querySelectorAll('[data-topic]').forEach(btn => {
  btn.addEventListener('click', () => {
    const t = btn.getAttribute('data-topic');
    state.topic = t;
    // update hash
    location.hash = t;
    renderPage(t);
  });
});

/* ===== Submenu Action ===== */
document.querySelectorAll('[data-toggle]').forEach(toggleBtn => {
  toggleBtn.addEventListener('click', () => {
    const id = toggleBtn.getAttribute('data-toggle');
    const parentLi = toggleBtn.closest('.has-children');
    parentLi.classList.toggle('open');
  });
});

/* ===== Colapse sidebar Action ===== */
collapseBtn.addEventListener('click', () => {
  document.body.classList.add('collapsed');
});
reopenBtn.addEventListener('click', () => {
  document.body.classList.remove('collapsed');
});

/* ===== Refresh all menu labels based on the current language =====
   This function maps each menu button that has a `data-topic` attribute
   to the corresponding `I18N[lang][topic].title`. It also updates small
   UI labels that are not tied to a page, such as the "Each window" toggle
   and the "(Collapse menu)" button.
*/
function refreshMenuLabels(lang){
  // Update every menu/submenu item that declares a data-topic
  document.querySelectorAll('[data-topic]').forEach(btn => {
    const topic = btn.getAttribute('data-topic');
    const def = I18N?.[lang]?.[topic];
    if (def && def.title){
      // Prefer writing into <span class="txt"> if present; otherwise use the element itself
      const labelEl = btn.querySelector('.txt') || btn;
      // Some titles include HTML entities (e.g., &amp;). Using innerHTML keeps them intact.
      labelEl.innerHTML = def.title;
    }
  });

  // Update non-page UI strings
  const eachWinTxt = document.querySelector('[data-toggle="sub-windows"] .txt');
  if (eachWinTxt) eachWinTxt.textContent = I18N[lang].ui.menuEachWindow;

  const collapseTxt = document.getElementById('collapseBtn')?.querySelector('.txt');
  if (collapseTxt) collapseTxt.textContent = I18N[lang].ui.collapse;
}

function setLang(lang){
  if (!I18N[lang]) return;
  state.lang = lang;
  localStorage.setItem(LANG_KEY, lang);
  // Keep same topic after change language
  renderPage(state.topic);
  // Reflect the language in the <html lang="..."> attribute (accessibility/SEO)
  document.documentElement.setAttribute('lang', lang === 'pt' ? 'pt-BR' : 'en');

  // Refresh every menu label and UI microcopy according to I18N
  refreshMenuLabels(lang);
}
btnPT.addEventListener('click', () => setLang('pt'));
btnEN.addEventListener('click', () => setLang('en'));

/* ===== Starting ===== */
readHash();
setLang(state.lang);      // define language and render the UI
renderPage(state.topic);  // start with the initial content / state
