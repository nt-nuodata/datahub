import { green, orange, red } from '@ant-design/colors';
import { Image, Popover } from 'antd';
import styled from 'styled-components/macro';
import moment from 'moment-timezone';
import React from 'react';
import { QuestionCircleOutlined } from '@ant-design/icons';
import { toLocalDateTimeString, toRelativeTimeString } from '../../../../../shared/time/timeUtils';
import { ANTD_GRAY } from '../../../constants';
import { useEntityData } from '../../../EntityContext';
import { useEntityRegistry } from '../../../../../useEntityRegistry';
import { getPlatformName } from '../../../utils';
import { getDisplayedEntityType } from '../header/PlatformContent/PlatformContentContainer';

const StyledDot = styled.div<{ color: string }>`
    border: 1px solid ${ANTD_GRAY[5]};
    border-radius: 50%;
    background-color: ${(props) => props.color};
    width: 10px;
    height: 10px;
    margin-right: 8px;
    vertical-align: middle;
`;

const Title = styled.div`
    font-size: 12px;
    font-weight: bold;
    display: flex;
    align-items: center;
    margin-bottom: 5px;

    ${StyledDot} {
        margin: 0 8px 0 0;
    }
`;

const PopoverContentWrapper = styled.div``;

const MainContent = styled.div`
    align-items: center;
    display: flex;
    color: ${ANTD_GRAY[8]};
`;

const RelativeDescription = styled.div`
    align-items: center;
    display: flex;
    margin-bottom: 5px;
`;

const TrustIndexRelativeDescription = styled.div`
    margin-top: 5px
    margin-bottom: 5px;
    max-width: 400px;
`;

const SubText = styled.div`
    color: ${ANTD_GRAY[7]};
    font-size: 10px;
    font-style: italic;
`;

const HelpIcon = styled(QuestionCircleOutlined)`
    color: ${ANTD_GRAY[7]};
    margin-left: 7px;
    font-size: 10px;
`;

const HelpHeader = styled.div`
    margin-bottom: 5px;
    max-width: 250px;
`;

const TrustIndexHeader = styled.div`
    margin-bottom: 5px;
    max-width: 400px;
`;

const LastIngestedWrapper = styled.div`
    display: flex;
    align-items: center;
`;

const TrustIndexWrapper = styled.div`
    display: flex;
    align-items: center;
`;

const TooltipSection = styled.div`
    align-items: center;
    display: flex;
    margin-bottom: 5px;
`;

const PreviewImage = styled(Image)`
    max-height: 9px;
    width: auto;
    object-fit: contain;
    background-color: transparent;
    padding-left: 1px;
`;

function TooltipContent() {
    return (
        <div>
            <TooltipSection>
                <StyledDot color={green[5]} /> Synchronized in the&nbsp;<b>past week</b>
            </TooltipSection>
            <TooltipSection>
                <StyledDot color={orange[5]} /> Synchronized in the&nbsp;<b>past month</b>
            </TooltipSection>
            <TooltipSection>
                <StyledDot color={red[5]} /> Synchronized&nbsp;<b>more than a month ago</b>
            </TooltipSection>
        </div>
    );
}
function TrustIndexTooltipContent() {
    return (
        <div>
            <TooltipSection>
                <StyledDot color={red[5]} /><b>Low&nbsp;</b> Trust Index&nbsp;(Trust Index is less than 50%)
            </TooltipSection>
            <TooltipSection>
                <StyledDot color={orange[5]} /> <b>Moderate&nbsp;</b> Trust Index&nbsp;(Trust Index lies between 50% and 80%)
            </TooltipSection>
            <TooltipSection>
                <StyledDot color={green[5]} /> <b>High&nbsp;</b> Trust Index&nbsp;(Trust Index is greater than or equal to 80%)
            </TooltipSection>
        </div>
    );
}

export function getLastIngestedColor(lastIngested: number) {
    const lastIngestedDate = moment(lastIngested);
    if (lastIngestedDate.isAfter(moment().subtract(1, 'week'))) {
        return green[5];
    }
    if (lastIngestedDate.isAfter(moment().subtract(1, 'month'))) {
        return orange[5];
    }
    return red[5];
}

export function calculateTrustIndex(trust_index_number: number){
    if (trust_index_number < 50) {
        return "Dataset has Low Trust Index";
    }
    if (trust_index_number < 80 && trust_index_number >= 50) {
        return "Dataset has Moderate Trust Index";
    }
    return "Dataset has High Trust Index";
    
};
export function getTrustIndexColor(trust_index_number:number) {
    
    
    if (trust_index_number < 50) {
        return red[5];
    }
    if (trust_index_number < 80 && trust_index_number >= 50) {
        return orange[5];
    }
    return green[5];
    
    
}

interface Props {
    lastIngested: number;
}

function LastIngested({ lastIngested }: Props) {
    const { entityData, entityType } = useEntityData();
    const entityRegistry = useEntityRegistry();
    const displayedEntityType = getDisplayedEntityType(entityData, entityRegistry, entityType);
    const lastIngestedColor = getLastIngestedColor(lastIngested);
    const platformName = getPlatformName(entityData);
    const platformLogoUrl = entityData?.platform?.properties?.logoUrl;
    const propertiesData = entityData?.customProperties;
    console.log(entityData)
    const trust_val = propertiesData?.find(i => i?.key === "trust_index");
    const trust_index_value = (trust_val?.value)?.replace("%","")
    let trust_index_number!: number;
    if (trust_index_value !== undefined){
        trust_index_number = parseFloat(trust_index_value);
    }
    const trustIndexColor=getTrustIndexColor(trust_index_number)
    

    return (
        <><LastIngestedWrapper>
            <Popover
                placement="left"
                content={<PopoverContentWrapper>
                    <Title>
                        <StyledDot color={lastIngestedColor} />
                        Last Synchronized
                    </Title>
                    <RelativeDescription>
                        This {displayedEntityType.toLocaleLowerCase()} was last synchronized&nbsp;
                        <b>{toRelativeTimeString(lastIngested)}</b>
                    </RelativeDescription>
                    <SubText>Synchronized on {toLocalDateTimeString(lastIngested)}</SubText>
                </PopoverContentWrapper>}
            >
                <MainContent>
                    <StyledDot color={lastIngestedColor} />
                    Last synchronized&nbsp;
                    <b>{toRelativeTimeString(lastIngested)}</b>
                </MainContent>
            </Popover>
            <Popover
                title={<HelpHeader>
                    This represents the time that the entity was last synchronized with&nbsp;
                    {platformName ? (
                        <strong>
                            {platformLogoUrl && (
                                <>
                                    <PreviewImage preview={false} src={platformLogoUrl} alt={platformName} />
                                    &nbsp;
                                </>
                            )}
                            {platformName}
                        </strong>
                    ) : (
                        <>the source platform</>
                    )}
                </HelpHeader>}
                content={TooltipContent}
                placement="bottom"
            >
                <HelpIcon />
            </Popover>
        </LastIngestedWrapper>
        <TrustIndexWrapper>
        <Popover
                placement="left"
                content={<PopoverContentWrapper>
                    <Title>
                        <StyledDot color={trustIndexColor} />
                        Trust Index&nbsp;
                    </Title>
                    <TrustIndexRelativeDescription>
                        This dataset has a trust index value of&nbsp;<b>{trust_index_value}%</b>, which is a metric representing the degree to which this dataset adheres to governance compliance&nbsp;
                    </TrustIndexRelativeDescription>
                    <SubText>{calculateTrustIndex(trust_index_number)}</SubText>
                </PopoverContentWrapper>}
            >
                <MainContent>
                    <StyledDot color={trustIndexColor} />
                    Trust Index&nbsp;
                    <b>{trust_index_value}%</b>
                </MainContent>
            </Popover>
            <Popover
                title={<TrustIndexHeader>
                    This dataset has a trust index value of <b>{trust_index_value}%</b>, which is a metric representing the degree to which this dataset adheres to governance compliance&nbsp;
                </TrustIndexHeader>}
                content={TrustIndexTooltipContent}
                placement="bottom"
            >
                <HelpIcon />
            </Popover>
        
        </TrustIndexWrapper></>
    );
}

export default LastIngested;
