#include <cnoid/SimpleController>

class MyController : public cnoid::SimpleController {
  cnoid::BodyPtr ioBody;

public:
  virtual bool initialize(cnoid::SimpleControllerIO *io) override {
    ioBody = io->body();
    cnoid::Link *joint = ioBody->joint(1);

    joint->setActuationMode(cnoid::Link::JointVelocity);
    io->enableIO(joint);

    return true;
  }

  virtual bool start() override {
    cnoid::Link *joint = ioBody->joint(1);
    joint->dq_target() = 200;

    return true;
  }
};

CNOID_IMPLEMENT_SIMPLE_CONTROLLER_FACTORY(MyController)
