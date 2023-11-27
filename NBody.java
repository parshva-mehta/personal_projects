import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import javax.swing.*;



//Overall note: to whom it may concern: The project is not perfect and needs more debugging. The stars clump in the top right corner. 
//I believe this is due to the initial velocities and the program's time complexity being exponential due to multiple nested loops. 

//The program one by one has the stars affect surrounding stars nearby, this is once again due to the for loop being slow and inefficient. 

public class NBody extends Canvas implements ActionListener
{
    public int n;

    //initial pos
    public ArrayList<Integer> xCoord = new ArrayList<>();
    public ArrayList<Integer> yCoord = new ArrayList<>();
    public ArrayList<Integer> Mass = new ArrayList<>();
    public ArrayList<Color> setColor = new ArrayList<>();

    //change in postion dP = v * dt
    public ArrayList<Double> xVel = new ArrayList<>();
    public ArrayList<Double> yVel = new ArrayList<>();

    //change in velocity dV = a * dt


    public ArrayList<Double> xAcc = new ArrayList<>();
    public ArrayList<Double> yAcc = new ArrayList<>();


    
    public int size;
    public double dt;
    public double maxVel;
    public double maxMass;
    public double g;

    public void init(int n)
    {
        // Your initialization code here:
        this.n = n;
        for(int i = 0; i < n; i++){

            //initializing using Math.random
            int x = (int) (Math.random() * size);
            int y = (int) (Math.random() * size);
            int mass = (int) (Math.random() * maxMass + 1);
            int R = (int) (Math.random() * 255);
            int G = (int) (Math.random() * 255);
            int B = (int) (Math.random() * 255);
            double initVelX =(Math.random() * (2 * maxVel) - maxVel); 
            double initVelY =(Math.random() * (2 * maxVel) - maxVel); 


            Color color = new Color(R, G, B);

            xCoord.add(x);
            yCoord.add(y);
            setColor.add(color);
            Mass.add(mass);
            xVel.add(initVelX);
            yVel.add(initVelY);

        }
    }





    // Draw a circle centered at (x, y) with radius r
    public void drawCircle(Graphics g, int x, int y, int r)
    {
        int d = 2*r;
        g.fillOval(x - r, y - r, d, d);
    }

    public void paint(Graphics g)
    {
        // Clear the screen
        super.paint(g);

        // Your drawing code here:

        for(int i = 0; i < n; i++){
            g.setColor(setColor.get(i)); //using the index to group the attributes of each star
            drawCircle(g, xCoord.get(i), yCoord.get(i), Mass.get(i)/2);            
        }

    }

    public void actionPerformed(ActionEvent e)
    {
        // Your update code here:


        for(int j = 0; j < n; j++){
            double dV = 0;
            for(int k = 0; k < n; k++){
                if(j != k){ //making sure we arent calculating acceleration due to the same star (avoiding infinity based error)
                    double distX = xCoord.get(k) - xCoord.get(j); //calculating distance in the x direction
                    double distY = yCoord.get(k) - yCoord.get(j); //calculating distance in the y direction
                    
                    double r = Math.sqrt((distX * distX) + (distY * distY)); //calculating the magnitude 
                    if(r < 10){
                        r = 5; //setting r = 5 if stars get too close
                    }
    
                    double m1 = Mass.get(j); 
                    double m2 = Mass.get(k);
                    dV = (g * m1 * m2 * dt)/ (m1 * (r * r)); //using mass, magnutude and g to find the change in veloctiy

                    xAcc.add(dV);
                    yAcc.add(dV); //adding the change in veloctiy to an arraylist to access (acceleration)

                    if(distX < 0)
                        xVel.set(j, xVel.get(j) - (dt * xAcc.get(j)));
                    else
                        xVel.set(j, xVel.get(j) + (dt * xAcc.get(j)));  

                    if(distY < 0)
                        yVel.set(j, yVel.get(j) - (dt * xAcc.get(j)));
                    else
                        yVel.set(j, yVel.get(j) + (dt * xAcc.get(j)));
                    
                }
                
            }
        }

        for(int i = 0; i < n; i++){
            xCoord.set(i,(int) (xCoord.get(i) + (dt * xVel.get(i)))); //updating the coordinates
            yCoord.set(i,(int) (yCoord.get(i) + (dt * yVel.get(i))));
            
        }


        // Repaint the screen
        repaint();
        Toolkit.getDefaultToolkit().sync();
    }

    public static void main(String[] args)
    {
        JFrame frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        int n = Integer.parseInt(args[0]);

        NBody nbody = new NBody();
        nbody.setBackground(Color.BLACK);
        nbody.size = 1600;
        nbody.maxVel = 10;
        nbody.maxMass = 10;
        nbody.dt = 0.1;
        nbody.g = 10000;
        nbody.setPreferredSize(new Dimension(nbody.size, nbody.size));
        nbody.init(n);

        frame.add(nbody);
        frame.pack();

        Timer timer = new Timer(16, nbody);
        timer.start();

        frame.setVisible(true);
    }
}