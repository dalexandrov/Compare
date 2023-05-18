
package com.example.compare.nima;

import io.helidon.nima.webserver.WebServer;
import io.helidon.nima.webserver.http.HttpRouting;

/**
 * As simple as possible with a fixed port.
 */
public class Main {
    private Main() {
    }

    /**
     * Main method.
     *
     * @param args ignored
     */
    public static void main(String[] args) {

        WebServer.builder()
                .port(8080)
                .routing(Main::routing)
                .start();
    }

    /**
     * Set up HTTP routing.
     * This method is used from both unit and integration tests.
     *
     * @param router HTTP routing builder to configure routes for this service
     */
    static void routing(HttpRouting.Builder router) {
        router
                .register("/greet", new GreetService());
    }
}
