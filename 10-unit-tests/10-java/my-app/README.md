Seguendo le istruzioni https://maven.apache.org/guides/getting-started/maven-in-five-minutes.html è stato generato il progetto con il seguente comando

mvn archetype:generate -DgroupId=com.mycompany.app -DartifactId=my-app -DarchetypeArtifactId=maven-archetype-quickstart -DarchetypeVersion=1.5 -DinteractiveMode=false

Per eseguire solo i test: mvn test

Per creare il jar: mvn package

Per eseguire il jar: java -jar target/my-app-1.0-SNAPSHOT.jar
