# GraphicModelFURG

# Como executar

Tenha python3 instalado.
Primeiramente, temos um arquivo requirements.txt, então execute:

```bash
pip install -r requirements.txt
```

Então, execute o arquivo C3.py com:

```bash
python C3.py
```

## Como o sistema funciona
Utilizamos OpenGl para .... e Pygames para ...

### Itens implementados do zero:
* Projeção da camera (perspectiva/ortogonal) trocável ao pressionar a tecla P;
* Movimento de câmera por teclado (W,S para frente e trás, A,D para esquerda e direita, e E,Q para cima e baixo);
* Rotação de câmera por teclado (arrow-keys para mudar a rotação);


Projeto de Computação Gráfica - FURG
Este projeto é um ambiente virtual 3D desenvolvido com Pygame e PyOpenGL para a disciplina de Computação Gráfica. A cena renderiza um objeto 3D com câmera interativa e iluminação, aplicando diversos conceitos da área.

Integrantes:

Nome do Integrante 1 - Matrícula 1

Nome do Integrante 2 - Matrícula 2

(Opcional) Nome do Integrante 3 - Matrícula 3

Como o sistema funciona
O projeto utiliza uma combinação de tecnologias:

Pygame: Gerencia a janela, os eventos de teclado e o loop principal da aplicação.

OpenGL (via PyOpenGL): Responsável por toda a renderização 3D, incluindo iluminação, desenho de geometrias e gerenciamento de matrizes no pipeline de função fixa.

Como Executar
Instale as dependências:

```bash
pip install pygame numpy PyOpenGL PyOpenGL_accelerate
```

Execute o arquivo principal:

```bash
python nome_do_seu_arquivo.py
```
