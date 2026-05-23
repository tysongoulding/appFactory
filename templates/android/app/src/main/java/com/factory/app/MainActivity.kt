package com.factory.APP_ID_PLACEHOLDER

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AppFactoryTheme {
                AppFactoryDashboard()
            }
        }
    }
}

// Brand Tokens matching Monorepo Contract
val GoogleBrandGreen = Color(0xFF34A853)
val DarkSlateBackground = Color(0xFF0B0F19)
val GlassSurfaceColor = Color(0x0DFFFFFF)
val GlassBorderColor = Color(0x1AFFFFFF)

@Composable
fun AppFactoryDashboard() {
    val coroutineScope = rememberCoroutineScope()
    var isPressed by remember { mutableStateOf(false) }
    
    // Fetch values from system environment (populated securely by Vault OIDC integration)
    val apiEndpoint = System.getenv("VAULT_API_ENDPOINT") ?: "https://api.pulsar.factory.internal"
    val storageBucket = System.getenv("VAULT_GCS_BUCKET_NAME") ?: "factory-pulsar-assets"

    // Animation transition for micro-interactions
    val scale by animateFloatAsState(
        targetValue = if (isPressed) 0.98f else 1.0f,
        animationSpec = springSpec(),
        label = "scale"
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(DarkSlateBackground)
            .padding(24.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            // Header Section
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 40.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "APP FACTORY",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    color = GoogleBrandGreen,
                    letterSpacing = 4.sp
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Pulsar Engine",
                    fontSize = 32.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color.White
                )
            }

            // Glassmorphic Details Card
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .scale(scale)
                    .clip(RoundedCornerShape(24.dp))
                    .background(GlassSurfaceColor)
                    .border(1.dp, GlassBorderColor, RoundedCornerShape(24.dp))
                    .padding(24.dp)
            ) {
                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "SECURE SESSION",
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold,
                            color = GoogleBrandGreen,
                            modifier = Modifier
                                .background(GoogleBrandGreen.copy(alpha = 0.15f), RoundedCornerShape(4.dp))
                                .padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    Text(
                        text = "OIDC Authentication Verified",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.SemiBold,
                        color = Color.White
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    InfoField(label = "Vault Namespace", value = "secret/data/app-factory/app-03-pulsar")
                    InfoField(label = "Secure Host Address", value = apiEndpoint)
                    InfoField(label = "Storage Destination (GCS)", value = storageBucket)
                }
            }

            // Sync Button
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(56.dp)
                    .clip(RoundedCornerShape(16.dp))
                    .background(GoogleBrandGreen)
                    .clickable(
                        interactionSource = remember { MutableInteractionSource() },
                        indication = null
                    ) {
                        coroutineScope.launch {
                            isPressed = true
                            delay(100)
                            isPressed = false
                        }
                    },
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "Sync Infrastructure",
                    color = Color.White,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold
                )
            }
        }
    }
}

@Composable
fun InfoField(label: String, value: String) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Text(text = label, fontSize = 11.sp, color = Color.White.copy(alpha = 0.5f))
        Spacer(modifier = Modifier.height(2.dp))
        Text(text = value, fontSize = 14.sp, color = Color.White.copy(alpha = 0.9f))
        Spacer(modifier = Modifier.height(12.dp))
    }
}

@Composable
fun ColumnScope.InfoField(label: String, value: String) {
    Column(modifier = Modifier.fillMaxWidth()) {
        Text(text = label, fontSize = 11.sp, color = Color.White.copy(alpha = 0.5f))
        Spacer(modifier = Modifier.height(2.dp))
        Text(text = value, fontSize = 14.sp, color = Color.White.copy(alpha = 0.9f))
    }
}

fun springSpec(): SpringSpec<Float> {
    return spring(
        dampingRatio = Spring.DampingRatioMediumBouncy,
        stiffness = Spring.StiffnessLow
    )
}

@Composable
fun AppFactoryTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = GoogleBrandGreen,
            background = DarkSlateBackground,
            surface = GlassSurfaceColor
        ),
        content = content
    )
}
