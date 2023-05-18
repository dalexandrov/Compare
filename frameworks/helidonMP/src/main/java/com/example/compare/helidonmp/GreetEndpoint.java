package com.example.compare.helidonmp;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;

@Path("/greet")
public class GreetEndpoint {

    @Path("/")
    @GET
    public String greet() {
        return "Hello Helidon MP";
    }
}
