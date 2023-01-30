# ForensicView

<p>"ForensicView" is an interactive GeoData-Visualizer that provides an overview
over uploaded files with GeoData in it. This Repository was programmed during the module "IT-Forensik" at the "Leuphana
Universität" in  Lüneburg.</p>
<p>To use the prgramm follow the following steps:</p>
<ul>
<li>
<p>Clone Repository</p>

```git
gh repo clone paultepe/ForensicView
```
</li>
<li>
<b>Make sure Docker is running.</b><br>
<p>Build Docker image</p>

```bash
docker-compose -f demo.yml build
```
</li>
<li>
Start container

```bash
docker-compose -f demo.yml up
```
</li>
</ul>

<p>By default the programm has an admin user:</p>
    <ul>
        <li>Username: admin</li>
        <li>Passwort: administrator2023</li>
    </ul>

<p>Using the Admin-Panel, data can be loaded (demo data can be found in demo_files). 
To display the GeoData on the website press the analyse-button on the main page.</p>
<p>Beside the admin panel, multiple images can be uploaded directly into the
file system (user_data/images/<exact_device_name>) to provide batch processing. Import the images
to a specific device by clicking the "Bild-Import"-Button on the main page.
Make sure that the field "Asservat" and the corresponding folder matches an existing device from the database.</p>


<p>Most important directories/files:</p>
<ul>
    <li>data/templates</li>
    <li>forensik/case/analyze.py</li>
    <li>forensik/case/models.py</li>
    <li>forensik/case/urls.py</li>
    <li>forensik/case/views.py</li>
</ul>
