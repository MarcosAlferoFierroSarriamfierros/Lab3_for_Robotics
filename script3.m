% Crear el suscriptor al tópico de pose de Turtle1
% Crear el suscriptor al tópico de pose de Turtle1
poseSubscriber = rossubscriber('/turtle1/pose');

pause(1); % Espera un segundo para asegurarse de recibir el último mensaje

% Obtener el último mensaje de pose
latestPose = receive(poseSubscriber, 1); % Espera hasta recibir un mensaje

% Mostrar la posición y orientación de Turtle1
disp('Última pose de Turtle1:');
disp(['Posición (x, y): ', num2str(latestPose.X), ', ', num2str(latestPose.Y)]);
disp(['Orientación (z): ', num2str(latestPose.Theta)]);

% Crear un objeto de cliente de servicio para el servicio de teleportación absoluta
teleportClient = rossvcclient('/turtle1/teleport_absolute');

% Crear una solicitud de servicio
req = rosmessage(teleportClient);

% Establecer la nueva posición y orientación de Turtle1
req.X = 5; % Nueva posición en el eje X
req.Y = 5; % Nueva posición en el eje Y
req.Theta = pi/2; % Nueva orientación (en radianes)

% Llamar al servicio de teleportación absoluta para establecer la nueva pose de Turtle1
resp = call(teleportClient, req);

% Finalizar el nodo maestro de ROS
rosshutdown;
