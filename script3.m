%Nos suscribimos al tema de turtle1
poseSubscriber = rossubscriber('/turtle1/pose');

pause(1); 
% Mensaje con datos de a pose
latestPose = receive(poseSubscriber, 1); % Se hace una pausa hasta recibir un mensaje

% Mostrar la posición y orientación de la tortuga
disp('Última pose de Turtle1:');
disp(['Posición (x, y): ', num2str(latestPose.X), ', ', num2str(latestPose.Y)]);
disp(['Orientación (z): ', num2str(latestPose.Theta)]);
teleportClient = rossvcclient('/turtle1/teleport_absolute');
req = rosmessage(teleportClient);

% Ponemos una posiciòn random en la tortuga para ver que se mueva
req.X = 5; 
req.Y = 5; 
req.Theta = pi/2; % en rads
resp = call(teleportClient, req);
% Finalizamos nodo maestro de ROS
rosshutdown;
