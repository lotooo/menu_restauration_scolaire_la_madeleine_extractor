# menu_restauration_scolaire_la_madeleine_extractor

Script pour extraire les menus de la ville de la Madeleine et les envoyer dans un calendrier Caldav (de type framagenda/nextcloud)

Les pdfs sont accessibles sur le site de la mairie : https://www.ville-lamadeleine.fr/au-quotidien/enfance-ecole/restauration-scolaire

Ce script les extrait grâce à `BeautifulSoup`, le parse grâce à `pdfplubmer` et les envoie sur un calendrier grâce à `caldav`

## Comment l'utiliser ?

1. Créer un fichier `.env` avec les infos de connections au caldav :

```
export WEBDAV_URL=framagenda.org/remote.php/dav/calendars/toto/xxxx/
export WEBDAV_CAL=MenuCantineLaMadeleine
export WEBDAV_USER=toto
export WEBDAV_PASS=securedpassword
```

2. Lancer `.run.sh`

3. Enjoy
