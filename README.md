# ONoC-Ring-Topology-Optimization
Algorithm for optimizing ONoC ring topology networks with a congestion-aware heuristic algorithm simulated with OMNeT++.

## Steps to Set Up OMNeT++
- Download and Install OMNeT++:

Download OMNeT++ from the official website.
Follow the installation instructions for Windows.
Create a New Project:

Open OMNeT++ and create a new project using the IDE.
Set Up the Network Topology:

Define the ring topology and implement the congestion-aware heuristic routing algorithm.
Example Implementation
Step 1: Define the Network Topology in NED
Create a .ned file to define the ring topology:

ned
Copy code
network RingTopology
{
    parameters:
        int numNodes;
    submodules:
        node[numNodes]: Node;
    connections allowunconnected:
        for i=0..numNodes-1 {
            node[i].pppg++ <--> {delay = 2ms; datarate = 1Gbps;} <--> node[(i+1)%numNodes].pppg++;
        }
}
Step 2: Define the Node
Create a Node.ned file to define the node structure:

ned
Copy code
simple Node
{
    gates:
        input pppg[];
        output pppg[];
    parameters:
        @display("i=block/cogwheel");
}
Step 3: Implement the Congestion-Aware Heuristic Routing Algorithm
Create a C++ file for the routing logic (CongestionAwareRouting.cc):

cpp
Copy code
#include <omnetpp.h>
#include "CongestionAwareRouting_m.h"

using namespace omnetpp;

class CongestionAwareRouting : public cSimpleModule
{
  private:
    int numNodes;
    int threshold;
    std::vector<int> congestionLevels;

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    void updateCongestionLevels();
    int calculateThreshold();
    const char* findPath(int source, int destination);

  public:
    CongestionAwareRouting();
};

Define_Module(CongestionAwareRouting);

CongestionAwareRouting::CongestionAwareRouting() {}

void CongestionAwareRouting::initialize()
{
    numNodes = par("numNodes");
    threshold = calculateThreshold();
    congestionLevels.resize(numNodes, 0);
    scheduleAt(simTime() + 1, new cMessage("updateCongestion"));
}

void CongestionAwareRouting::handleMessage(cMessage *msg)
{
    if (strcmp(msg->getName(), "updateCongestion") == 0)
    {
        updateCongestionLevels();
        scheduleAt(simTime() + 1, msg);
    }
    else
    {
        // Handle incoming packets and route them
        cPacket *pkt = check_and_cast<cPacket *>(msg);
        int source = pkt->getArrivalGate()->getIndex();
        int destination = pkt->getKind(); // Assuming destination is set in the kind field
        const char* path = findPath(source, destination);
        send(pkt, path);
    }
}

void CongestionAwareRouting::updateCongestionLevels()
{
    // Simulate congestion update logic
    for (int i = 0; i < numNodes; ++i)
    {
        congestionLevels[i] = intuniform(0, 10);
    }
}

int CongestionAwareRouting::calculateThreshold()
{
    return numNodes / 2;
}

const char* CongestionAwareRouting::findPath(int source, int destination)
{
    int distanceCW = (destination - source + numNodes) % numNodes;
    int distanceCCW = (source - destination + numNodes) % numNodes;
    if (distanceCW > threshold)
        return "pppg$o[0]"; // Clockwise
    else if (distanceCCW > threshold)
        return "pppg$o[1]"; // Counterclockwise
    else
    {
        int cwCongestion = 0, ccwCongestion = 0;
        for (int i = 0; i < threshold; ++i)
        {
            cwCongestion += congestionLevels[(source + i) % numNodes];
            ccwCongestion += congestionLevels[(source - i + numNodes) % numNodes];
        }
        return (cwCongestion < ccwCongestion) ? "pppg$o[0]" : "pppg$o[1]";
    }
}
Step 4: Compile and Run the Simulation
Open the OMNeT++ IDE.
Create a new simulation configuration in the omnetpp.ini file:
ini
Copy code
[General]
network = RingTopology
numNodes = 10
Build and run the simulation using the IDE.
