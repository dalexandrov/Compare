
package com.example.compare.helidon;

import io.helidon.webserver.Routing;
import io.helidon.webserver.ServerRequest;
import io.helidon.webserver.ServerResponse;
import io.helidon.webserver.Service;

public class GreetService implements Service {
    @Override
    public void update(Routing.Rules rules) {
        rules.get("/", this::getMessageHandler);

    }

    private void getMessageHandler(ServerRequest request, ServerResponse response) {
        response.send("Hello Helidon");
    }
}