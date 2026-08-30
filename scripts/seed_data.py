from app.database.database import SessionLocal
from app.models.blocker_event import BlockerEvent


def seed_blocker_events():

    db = SessionLocal()

    try:

        # Avoid duplicate seed data while testing
        existing_count = (
            db.query(BlockerEvent).count()
        )

        if existing_count > 0:
            print(
                f"Blocker events already exist: "
                f"{existing_count} records."
            )
            return

        sample_events = [

            # ============================================
            # CRITICAL
            # CREATE TABLE
            # ============================================
            BlockerEvent(
                blocker_command="CREATE TABLE",
                blocker_database_name="AREDTSITF",
                blocker_host_name="sbox-utc-awt",
                blocker_login_name="QCmdUser",
                blocker_object_name="isp_QCmd_GetPendingTask",
                blocker_program_name=(
                    "ARE_QCSvc_27103_WS_DTS_OUT-"
                    "ARE_STG_AREDTSITF"
                ),
                blocker_schema_name="dbo",
                blocker_session_id="112",
                blocker_wait_type="PAGELATCH_EX",

                waiter_command="CREATE TABLE",
                waiter_database_name="INDDTSITF",
                waiter_host_name="sbox-utc-awt",
                waiter_login_name="QCmdUser",
                waiter_program_name=(
                    "IND_QCSvc_63204_WS_DTS_OUT-"
                    "IND_STG_INDDTSITF"
                ),
                waiter_session_id="3443",
                waiter_wait_type="PAGELATCH_EX",

                app="capella-fbm-wms-wmsdb-a-utc-awt",
                env="stage",
                instance="localhost:1433",
                job="integrations/mssql",
                node_name=(
                    "wmsdb-a-utc-awt-stage-westeurope"
                ),
                os="windows",
                product_id="capella-wms",
                provider="azure",
                region="westeurope",
                server_type="sql",
                sql_version="2019",
                user_metrics="waiter_wait_time_sec",

                queue_status="NEW"
            ),

            # ============================================
            # HIGH
            #
            # UPDATE + integrations/mssql
            # ============================================
            BlockerEvent(
                blocker_command="UPDATE",
                blocker_database_name="WMSDB",
                blocker_host_name="wms-stage-db",
                blocker_login_name="app_user",
                blocker_object_name="Shipment",
                blocker_program_name=(
                    "ShipmentProcessingService"
                ),
                blocker_schema_name="dbo",
                blocker_session_id="201",
                blocker_wait_type="LCK_M_X",

                waiter_command="SELECT",
                waiter_database_name="WMSDB",
                waiter_host_name="wms-stage-api",
                waiter_login_name="report_user",
                waiter_program_name="ShipmentTrackingAPI",
                waiter_session_id="912",
                waiter_wait_type="LCK_M_S",

                app="shipment-service",
                env="stage",
                instance="localhost:1433",
                job="integrations/mssql",
                node_name="wms-stage-node-1",
                os="windows",
                product_id="capella-wms",
                provider="azure",
                region="westeurope",
                server_type="sql",
                sql_version="2019",
                user_metrics="waiter_wait_time_sec",

                queue_status="NEW"
            ),

            # ============================================
            # MEDIUM
            #
            # SELECT blocker + UPDATE waiter
            # ============================================
            BlockerEvent(
                blocker_command="SELECT",
                blocker_database_name="WMSDB",
                blocker_host_name="wms-stage-db",
                blocker_login_name="report_user",
                blocker_object_name="OrderHeader",
                blocker_program_name=(
                    "WarehouseReportService"
                ),
                blocker_schema_name="dbo",
                blocker_session_id="301",
                blocker_wait_type="LCK_M_S",

                waiter_command="UPDATE",
                waiter_database_name="WMSDB",
                waiter_host_name="wms-stage-api",
                waiter_login_name="app_user",
                waiter_program_name="OrderUpdateService",
                waiter_session_id="1001",
                waiter_wait_type="LCK_M_X",

                app="warehouse-service",
                env="stage",
                instance="localhost:1433",
                job="warehouse/job",
                node_name="wms-stage-node-2",
                os="windows",
                product_id="capella-wms",
                provider="azure",
                region="westeurope",
                server_type="sql",
                sql_version="2019",
                user_metrics="waiter_wait_time_sec",

                queue_status="NEW"
            ),

            # ============================================
            # LOW
            # ============================================
            BlockerEvent(
                blocker_command="SELECT",
                blocker_database_name="WMSDB",
                blocker_host_name="wms-stage-db",
                blocker_login_name="report_user",
                blocker_object_name="Product",
                blocker_program_name=(
                    "ProductReportService"
                ),
                blocker_schema_name="dbo",
                blocker_session_id="401",
                blocker_wait_type="LCK_M_S",

                waiter_command="SELECT",
                waiter_database_name="WMSDB",
                waiter_host_name="wms-stage-api",
                waiter_login_name="report_user",
                waiter_program_name="ProductDashboard",
                waiter_session_id="1020",
                waiter_wait_type="LCK_M_S",

                app="reporting-service",
                env="stage",
                instance="localhost:1433",
                job="reporting/job",
                node_name="wms-stage-node-3",
                os="windows",
                product_id="capella-wms",
                provider="azure",
                region="westeurope",
                server_type="sql",
                sql_version="2019",
                user_metrics="waiter_wait_time_sec",

                queue_status="NEW"
            )
        ]

        db.add_all(sample_events)

        db.commit()

        print(
            f"Successfully inserted "
            f"{len(sample_events)} blocker events."
        )

    except Exception as exc:

        db.rollback()

        print(
            f"Failed to seed blocker events: {exc}"
        )

    finally:

        db.close()


if __name__ == "__main__":
    seed_blocker_events()