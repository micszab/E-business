package com.example

import io.ktor.client.*
import io.ktor.client.engine.cio.*
import kotlinx.coroutines.runBlocking
import net.dv8tion.jda.api.JDABuilder
import net.dv8tion.jda.api.entities.Activity
import net.dv8tion.jda.api.events.message.MessageReceivedEvent
import net.dv8tion.jda.api.hooks.ListenerAdapter
import net.dv8tion.jda.api.requests.GatewayIntent
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

fun main() {
    // Initialize Ktor client
    val ktorClient = HttpClient(CIO)
    
    // Discord bot token
    val token = "YOUR_TOKEN_HERE"
    
    // Initialize JDA with Ktor client
    val jda = JDABuilder.createDefault(token)
        .setActivity(Activity.playing("Ready"))
        .enableIntents(GatewayIntent.MESSAGE_CONTENT)
        .addEventListeners(MessageListener(ktorClient))
        .build()
    
    println("Bot is now running!")
}

class MessageListener(private val ktorClient: HttpClient) : ListenerAdapter() {
    override fun onMessageReceived(event: MessageReceivedEvent) {
        if (event.author.isBot) return
        
        val message = event.message.contentRaw
        
        // Use mentions.users instead of mentionedUsers
        if (event.message.mentions.users.contains(event.jda.selfUser) || 
            message.startsWith("!bot")) {
            
            if (message.contains("time")) {
                val currentTime = LocalDateTime.now()
                val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
                val formattedTime = currentTime.format(formatter)
                event.channel.sendMessage("Current time: $formattedTime").queue()
            } else {
                event.channel.sendMessage("Hello! Use the command with 'time' to see the current time").queue()
            }
        }
    }
}