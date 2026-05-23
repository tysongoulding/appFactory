package com.factory.APP_ID_PLACEHOLDER

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.blur
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                ARSpaceBeamApp()
            }
        }
    }
}

@Composable
fun ARSpaceBeamApp() {
    val context = LocalContext.current
    var hasCameraPermission by remember {
        mutableStateOf(
            ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED
        )
    }
    var hasLocationPermission by remember {
        mutableStateOf(
            ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
        )
    }

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        hasCameraPermission = permissions[Manifest.permission.CAMERA] ?: hasCameraPermission
        hasLocationPermission = permissions[Manifest.permission.ACCESS_FINE_LOCATION] ?: hasLocationPermission
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF0F172A)) // Slate 900
    ) {
        if (hasCameraPermission && hasLocationPermission) {
            ARViewerScreen()
        } else {
            PermissionRequestScreen {
                launcher.launch(
                    arrayOf(
                        Manifest.permission.CAMERA,
                        Manifest.permission.ACCESS_FINE_LOCATION
                    )
                )
            }
        }
    }
}

@Composable
fun PermissionRequestScreen(onRequestPermissions: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Geospatial AR",
            fontSize = 32.sp,
            fontWeight = FontWeight.Bold,
            color = Color.White
        )
        Spacer(modifier = Modifier.height(12.dp))
        Text(
            text = "This application requires Camera and high-accuracy GPS permissions to anchor the spatial beam of light.",
            fontSize = 16.sp,
            color = Color(0xFF94A3B8), // Slate 400
            modifier = Modifier.padding(horizontal = 16.dp)
        )
        Spacer(modifier = Modifier.height(32.dp))
        Button(
            onClick = onRequestPermissions,
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF34A853)), // Brand Green
            shape = RoundedCornerShape(12.dp)
        ) {
            Text("Grant Permissions", color = Color.White, fontWeight = FontWeight.SemiBold)
        }
    }
}

@Composable
fun ARViewerScreen() {
    var vpsStatus by remember { mutableStateOf("Localizing") } // Localizing, Tracking, LowAccuracy
    var targetLocation by remember { mutableStateOf("Lat: 37.7749, Lon: -122.4194 (120m away)") }
    var beamAltitude by remember { mutableStateOf(100000.0) } // Height of beam in meters

    // Animate the beam status
    LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(3000)
        vpsStatus = "Tracking"
    }

    Box(modifier = Modifier.fillMaxSize()) {
        // Mock Camera View / AR Sceneview
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0xFF030712)) // Dark mock camera view
        ) {
            // Simulated space beam in 3D AR space
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .width(4.dp)
                    .align(Alignment.Center)
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(
                                Color(0x0034A853), // Transparent at top
                                Color(0xFF34A853), // Neon green glow
                                Color(0xAA34A853)  // Semi-transparent at base
                            )
                        )
                    )
            )
        }

        // Overlay status panel (Glassmorphic)
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.TopCenter)
                .padding(16.dp)
                .clip(RoundedCornerShape(16.dp))
                .background(Color(0x22FFFFFF))
                .border(1.dp, Color(0x33FFFFFF), RoundedCornerShape(16.dp))
                .padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "VPS STATUS:",
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF94A3B8),
                    fontSize = 12.sp
                )
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(if (vpsStatus == "Tracking") Color(0xFF34A853) else Color(0xFFEAB308))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(
                        text = vpsStatus.uppercase(),
                        fontWeight = FontWeight.Bold,
                        color = Color.White,
                        fontSize = 10.sp
                    )
                }
            }
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = "TARGET BEAM",
                fontSize = 10.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF94A3B8)
            )
            Text(
                text = targetLocation,
                fontSize = 14.sp,
                fontWeight = FontWeight.Medium,
                color = Color.White
            )
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = "BEAM ALTITUDE: ${beamAltitude.toInt()}m (Space Boundary)",
                fontSize = 12.sp,
                color = Color(0xFF34A853),
                fontWeight = FontWeight.SemiBold
            )
        }
    }
}
