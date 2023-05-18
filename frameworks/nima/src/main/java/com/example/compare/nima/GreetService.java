
package com.example.compare.nima;

import io.helidon.nima.webserver.http.HttpRules;
import io.helidon.nima.webserver.http.HttpService;
import io.helidon.nima.webserver.http.ServerRequest;
import io.helidon.nima.webserver.http.ServerResponse;

public class GreetService implements HttpService {

    @Override
    public void routing(HttpRules rules) {
        rules.get("/", this::getMessageHandler);
    }

    private void getMessageHandler(ServerRequest request, ServerResponse response) {
        response.send("Hello Nima");
    }
}